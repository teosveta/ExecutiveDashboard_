import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.validation_report = {}
        
    def validate_csv(self, df):
        report = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        if df is None or df.empty:
            report['valid'] = False
            report['errors'].append('File is empty or could not be read')
            return report
        
        report['info']['rows'] = len(df)
        report['info']['columns'] = len(df.columns)
        report['info']['column_names'] = list(df.columns)
        
        date_columns = self._detect_date_columns(df)
        if date_columns:
            report['info']['date_columns'] = date_columns
        else:
            report['warnings'].append('No date column detected. Time-series analysis may be limited.')
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        report['info']['numeric_columns'] = numeric_columns
        
        if not numeric_columns:
            report['warnings'].append('No numeric columns found. Limited analysis available.')
        
        missing_data = df.isnull().sum()
        if missing_data.any():
            missing_cols = missing_data[missing_data > 0].to_dict()
            report['warnings'].append(f'Missing data found in columns: {list(missing_cols.keys())}')
            report['info']['missing_data'] = missing_cols
        
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            report['warnings'].append(f'{duplicate_rows} duplicate rows found')
            report['info']['duplicates'] = duplicate_rows
        
        return report
    
    def _detect_date_columns(self, df):
        date_columns = []
        
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                date_columns.append(col)
                continue
            
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(10), errors='coerce')
                    non_null = df[col].head(10).notna().sum()
                    if non_null > 5:
                        date_columns.append(col)
                except:
                    pass
        
        return date_columns
    
    def clean_data(self, df):
        cleaned_df = df.copy()
        
        date_columns = self._detect_date_columns(cleaned_df)
        for col in date_columns:
            try:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            except:
                pass
        
        numeric_columns = cleaned_df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if cleaned_df[col].isnull().sum() > 0:
                median_value = cleaned_df[col].median()
                cleaned_df[col].fillna(median_value, inplace=True)
        
        categorical_columns = cleaned_df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col not in date_columns and cleaned_df[col].isnull().sum() > 0:
                mode_value = cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else 'Unknown'
                cleaned_df[col].fillna(mode_value, inplace=True)
        
        cleaned_df = cleaned_df.drop_duplicates()
        
        for col in numeric_columns:
            Q1 = cleaned_df[col].quantile(0.25)
            Q3 = cleaned_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            outliers = ((cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound)).sum()
            if outliers > 0 and outliers < len(cleaned_df) * 0.05:
                cleaned_df[col] = cleaned_df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return cleaned_df
    
    def process_uploaded_data(self, uploaded_file):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                return None, {'valid': False, 'errors': ['Unsupported file format. Please upload CSV or Excel files.']}
            
            self.original_data = df.copy()
            
            validation_report = self.validate_csv(df)
            
            if validation_report['valid']:
                self.data = self.clean_data(df)
            else:
                self.data = df
            
            self.validation_report = validation_report
            
            return self.data, validation_report
            
        except Exception as e:
            return None, {'valid': False, 'errors': [f'Error processing file: {str(e)}']}
    
    def get_summary_statistics(self, df):
        if df is None or df.empty:
            return None
        
        summary = {}
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary['numeric'] = df[numeric_cols].describe()
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary['categorical'] = {}
            for col in categorical_cols[:10]:
                summary['categorical'][col] = df[col].value_counts().head(10).to_dict()
        
        return summary
    
    def detect_key_metrics(self, df):
        if df is None or df.empty:
            return {}
        
        metrics = {
            'revenue_columns': [],
            'customer_columns': [],
            'date_columns': [],
            'performance_columns': []
        }
        
        revenue_keywords = ['revenue', 'sales', 'income', 'mrr', 'arr', 'earnings']
        customer_keywords = ['customer', 'user', 'client', 'subscriber']
        performance_keywords = ['profit', 'margin', 'growth', 'rate', 'score', 'satisfaction']
        
        for col in df.columns:
            col_lower = col.lower()
            
            if any(keyword in col_lower for keyword in revenue_keywords):
                metrics['revenue_columns'].append(col)
            
            if any(keyword in col_lower for keyword in customer_keywords):
                metrics['customer_columns'].append(col)
            
            if any(keyword in col_lower for keyword in performance_keywords):
                metrics['performance_columns'].append(col)
        
        metrics['date_columns'] = self._detect_date_columns(df)
        
        return metrics
