import pandas as pd
from datetime import datetime
from utils.database import Dataset, ForecastResult, Alert, AnalyticsResult, DataConnection, SessionLocal
import json

class DataStorage:
    
    def __init__(self):
        self.session = SessionLocal()
    
    def save_dataset(self, df, name, description="", source_type="upload"):
        try:
            existing = self.session.query(Dataset).filter(Dataset.name == name).first()
            
            if existing:
                existing.data = df.to_json(orient='records', date_format='iso')
                existing.description = description
                existing.source_type = source_type
                existing.updated_at = datetime.utcnow()
                existing.dataset_metadata = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
                }
                dataset = existing
            else:
                dataset = Dataset.from_dataframe(df, name, description, source_type)
                self.session.add(dataset)
            
            self.session.commit()
            return dataset.id
        except Exception as e:
            self.session.rollback()
            raise e
    
    def load_dataset(self, dataset_id):
        try:
            dataset = self.session.query(Dataset).filter(Dataset.id == dataset_id).first()
            if dataset:
                return dataset.to_dataframe()
            return None
        except Exception as e:
            raise e
    
    def get_dataset_by_name(self, name):
        try:
            dataset = self.session.query(Dataset).filter(Dataset.name == name).first()
            if dataset:
                return dataset.to_dataframe(), dataset.id
            return None, None
        except Exception as e:
            raise e
    
    def list_datasets(self):
        try:
            datasets = self.session.query(Dataset).order_by(Dataset.updated_at.desc()).all()
            return [{
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'source_type': d.source_type,
                'rows': d.dataset_metadata.get('rows', 0) if d.dataset_metadata else 0,
                'created_at': d.created_at,
                'updated_at': d.updated_at
            } for d in datasets]
        except Exception as e:
            raise e
    
    def delete_dataset(self, dataset_id):
        try:
            dataset = self.session.query(Dataset).filter(Dataset.id == dataset_id).first()
            if dataset:
                self.session.delete(dataset)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
    
    def save_forecast(self, dataset_id, metric_name, method, forecast_data, confidence_level="Medium", r2_score=None, parameters=None):
        try:
            forecast = ForecastResult(
                dataset_id=dataset_id,
                metric_name=metric_name,
                method=method,
                forecast_data=json.dumps(forecast_data),
                confidence_level=confidence_level,
                r2_score=r2_score,
                parameters=parameters or {}
            )
            self.session.add(forecast)
            self.session.commit()
            return forecast.id
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_forecast_history(self, dataset_id, metric_name):
        try:
            forecasts = self.session.query(ForecastResult).filter(
                ForecastResult.dataset_id == dataset_id,
                ForecastResult.metric_name == metric_name
            ).order_by(ForecastResult.created_at.desc()).limit(10).all()
            
            return [{
                'id': f.id,
                'method': f.method,
                'confidence_level': f.confidence_level,
                'r2_score': f.r2_score,
                'created_at': f.created_at,
                'data': f.to_dict()
            } for f in forecasts]
        except Exception as e:
            raise e
    
    def save_alert(self, name, metric_name, condition_type, threshold_value, email_recipients):
        try:
            alert = Alert(
                name=name,
                metric_name=metric_name,
                condition_type=condition_type,
                threshold_value=threshold_value,
                email_recipients=email_recipients
            )
            self.session.add(alert)
            self.session.commit()
            return alert.id
        except Exception as e:
            self.session.rollback()
            raise e
    
    def list_alerts(self, active_only=True):
        try:
            query = self.session.query(Alert)
            if active_only:
                query = query.filter(Alert.is_active == True)
            
            alerts = query.order_by(Alert.created_at.desc()).all()
            return [{
                'id': a.id,
                'name': a.name,
                'metric_name': a.metric_name,
                'condition_type': a.condition_type,
                'threshold_value': a.threshold_value,
                'email_recipients': a.email_recipients,
                'is_active': a.is_active,
                'trigger_count': a.trigger_count,
                'last_triggered': a.last_triggered
            } for a in alerts]
        except Exception as e:
            raise e
    
    def update_alert(self, alert_id, **kwargs):
        try:
            alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                for key, value in kwargs.items():
                    if hasattr(alert, key):
                        setattr(alert, key, value)
                alert.updated_at = datetime.utcnow()
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
    
    def delete_alert(self, alert_id):
        try:
            alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                self.session.delete(alert)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
    
    def save_analytics_result(self, dataset_id, analysis_type, result_data, parameters=None):
        try:
            result = AnalyticsResult(
                dataset_id=dataset_id,
                analysis_type=analysis_type,
                result_data=json.dumps(result_data),
                parameters=parameters or {}
            )
            self.session.add(result)
            self.session.commit()
            return result.id
        except Exception as e:
            self.session.rollback()
            raise e
    
    def save_data_connection(self, name, connection_type, connection_config):
        try:
            connection = DataConnection(
                name=name,
                connection_type=connection_type,
                connection_config=connection_config
            )
            self.session.add(connection)
            self.session.commit()
            return connection.id
        except Exception as e:
            self.session.rollback()
            raise e
    
    def list_data_connections(self):
        try:
            connections = self.session.query(DataConnection).filter(
                DataConnection.is_active == True
            ).order_by(DataConnection.updated_at.desc()).all()
            
            return [{
                'id': c.id,
                'name': c.name,
                'connection_type': c.connection_type,
                'last_sync': c.last_sync,
                'created_at': c.created_at
            } for c in connections]
        except Exception as e:
            raise e
    
    def __del__(self):
        self.session.close()
