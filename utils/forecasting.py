import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

class ForecastingEngine:
    
    def __init__(self):
        self.model = None
        
    def moving_average_forecast(self, data, window=7, periods=30):
        if len(data) < window:
            return None
        
        ma = data.rolling(window=window).mean()
        last_ma = ma.iloc[-1]
        
        forecast = [last_ma] * periods
        
        return {
            'forecast': forecast,
            'method': f'{window}-day Moving Average',
            'confidence': 'Medium'
        }
    
    def linear_regression_forecast(self, data, periods=30):
        if len(data) < 10:
            return None
        
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_X = np.arange(len(data), len(data) + periods).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        y_pred = model.predict(X)
        r2_score = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2))
        
        return {
            'forecast': forecast.tolist(),
            'method': 'Linear Regression',
            'confidence': 'High' if r2_score > 0.7 else 'Medium',
            'r2_score': r2_score,
            'trend': 'Increasing' if model.coef_[0] > 0 else 'Decreasing'
        }
    
    def polynomial_regression_forecast(self, data, periods=30, degree=2):
        if len(data) < 15:
            return None
        
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values
        
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        future_X = np.arange(len(data), len(data) + periods).reshape(-1, 1)
        future_X_poly = poly_features.transform(future_X)
        forecast = model.predict(future_X_poly)
        
        y_pred = model.predict(X_poly)
        r2_score = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2))
        
        return {
            'forecast': forecast.tolist(),
            'method': f'Polynomial Regression (degree {degree})',
            'confidence': 'High' if r2_score > 0.75 else 'Medium',
            'r2_score': r2_score
        }
    
    def exponential_smoothing_forecast(self, data, alpha=0.3, periods=30):
        if len(data) < 5:
            return None
        
        smoothed = [data.iloc[0]]
        
        for i in range(1, len(data)):
            smoothed_value = alpha * data.iloc[i] + (1 - alpha) * smoothed[-1]
            smoothed.append(smoothed_value)
        
        forecast = [smoothed[-1]] * periods
        
        return {
            'forecast': forecast,
            'method': f'Exponential Smoothing (α={alpha})',
            'confidence': 'Medium'
        }
    
    def prophet_forecast(self, df, column, date_column='Date', periods=30):
        try:
            if df is None or df.empty or column not in df.columns:
                return None
            
            if len(df) < 10:
                return None
            
            df_prophet = pd.DataFrame({
                'ds': pd.to_datetime(df[date_column]),
                'y': df[column]
            })
            
            df_prophet = df_prophet.dropna()
            
            if len(df_prophet) < 10:
                return None
            
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05
            )
            
            model.fit(df_prophet)
            
            future = model.make_future_dataframe(periods=periods)
            forecast_result = model.predict(future)
            
            forecast_values = forecast_result['yhat'].tail(periods).tolist()
            lower_bound = forecast_result['yhat_lower'].tail(periods).tolist()
            upper_bound = forecast_result['yhat_upper'].tail(periods).tolist()
            
            last_date = pd.to_datetime(df[date_column].iloc[-1])
            forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='D')[1:]
            
            return {
                'forecast': forecast_values,
                'method': 'Prophet (Facebook)',
                'confidence': 'High',
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'forecast_dates': forecast_dates.tolist(),
                'has_confidence_interval': True
            }
        except Exception as e:
            return None
    
    def arima_forecast(self, df, column, date_column='Date', periods=30, order=(1, 1, 1)):
        try:
            if df is None or df.empty or column not in df.columns:
                return None
            
            if len(df) < 20:
                return None
            
            df_sorted = df.copy()
            if date_column in df.columns:
                df_sorted = df_sorted.sort_values(date_column)
            
            data = df_sorted[column].dropna()
            
            if len(data) < 20:
                return None
            
            model = ARIMA(data, order=order)
            fitted_model = model.fit()
            
            forecast_result = fitted_model.forecast(steps=periods)
            
            if hasattr(fitted_model, 'get_forecast'):
                forecast_obj = fitted_model.get_forecast(steps=periods)
                conf_int = forecast_obj.conf_int()
                lower_bound = conf_int.iloc[:, 0].tolist()
                upper_bound = conf_int.iloc[:, 1].tolist()
                has_conf_int = True
            else:
                lower_bound = None
                upper_bound = None
                has_conf_int = False
            
            last_date = pd.to_datetime(df_sorted[date_column].iloc[-1])
            forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='D')[1:]
            
            return {
                'forecast': forecast_result.tolist(),
                'method': f'ARIMA{order}',
                'confidence': 'High',
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'has_confidence_interval': has_conf_int,
                'forecast_dates': forecast_dates.tolist(),
                'aic': fitted_model.aic,
                'bic': fitted_model.bic
            }
        except Exception as e:
            return None
    
    def forecast_metric(self, df, column, date_column='Date', periods=30, method='auto'):
        if df is None or df.empty or column not in df.columns:
            return None
        
        df_sorted = df.copy()
        if date_column in df.columns:
            df_sorted = df_sorted.sort_values(date_column)
        
        data = df_sorted[column].dropna()
        
        if len(data) < 10:
            return None
        
        if method == 'auto':
            lr_result = self.linear_regression_forecast(data, periods)
            if lr_result and lr_result.get('r2_score', 0) > 0.6:
                method = 'linear'
            else:
                method = 'moving_average'
        
        if method == 'linear':
            result = self.linear_regression_forecast(data, periods)
        elif method == 'polynomial':
            result = self.polynomial_regression_forecast(data, periods)
        elif method == 'moving_average':
            result = self.moving_average_forecast(data, periods=periods)
        elif method == 'exponential':
            result = self.exponential_smoothing_forecast(data, periods=periods)
        elif method == 'prophet':
            result = self.prophet_forecast(df_sorted, column, date_column, periods)
        elif method == 'arima':
            result = self.arima_forecast(df_sorted, column, date_column, periods)
        else:
            result = self.linear_regression_forecast(data, periods)
        
        if result is None:
            result = self.moving_average_forecast(data, periods=periods)
        
        if result is None:
            return None
        
        if date_column in df.columns and 'forecast_dates' not in result:
            last_date = pd.to_datetime(df_sorted[date_column].iloc[-1])
            date_range = pd.date_range(start=last_date, periods=periods+1, freq='D')[1:]
            result['forecast_dates'] = date_range.tolist()
        
        result['historical_data'] = data.tail(90).tolist()
        
        return result
    
    def compare_forecasts(self, df, column, date_column='Date', periods=30):
        methods = ['linear', 'prophet', 'arima', 'exponential']
        results = {}
        
        for method in methods:
            forecast_result = self.forecast_metric(df, column, date_column, periods, method)
            if forecast_result:
                results[method] = forecast_result
        
        return results
    
    def calculate_growth_rate(self, data, period='monthly'):
        if len(data) < 2:
            return None
        
        recent_value = data.iloc[-1]
        previous_value = data.iloc[0]
        
        if previous_value == 0:
            return None
        
        growth_rate = ((recent_value - previous_value) / previous_value) * 100
        
        return {
            'growth_rate': round(growth_rate, 2),
            'period': period,
            'recent_value': recent_value,
            'previous_value': previous_value
        }
    
    def detect_trends(self, data):
        if len(data) < 10:
            return None
        
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        slope = model.coef_[0]
        
        recent_mean = data.tail(10).mean()
        older_mean = data.head(10).mean()
        
        if slope > 0 and recent_mean > older_mean:
            trend = 'Strong Upward Trend'
        elif slope > 0:
            trend = 'Moderate Upward Trend'
        elif slope < 0 and recent_mean < older_mean:
            trend = 'Strong Downward Trend'
        elif slope < 0:
            trend = 'Moderate Downward Trend'
        else:
            trend = 'Stable'
        
        volatility = data.std() / data.mean() * 100 if data.mean() != 0 else 0
        
        return {
            'trend': trend,
            'slope': slope,
            'volatility': round(volatility, 2),
            'recent_average': round(recent_mean, 2),
            'overall_average': round(data.mean(), 2)
        }
