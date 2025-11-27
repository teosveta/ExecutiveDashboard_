import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import pandas as pd
import json

DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    # Use SQLite as default database if no DATABASE_URL is provided
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dashboard_data.db')
    DATABASE_URL = f'sqlite:///{db_path}'

# Different connection args for SQLite vs other databases
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

class Dataset(Base):
    __tablename__ = 'datasets'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    source_type = Column(String(50))
    data = Column(Text)
    dataset_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dataframe(self):
        if self.data:
            return pd.read_json(self.data)
        return None
    
    @staticmethod
    def from_dataframe(df, name, description="", source_type="upload"):
        data_json = df.to_json(orient='records', date_format='iso')
        dataset_metadata = {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        return Dataset(
            name=name,
            description=description,
            source_type=source_type,
            data=data_json,
            dataset_metadata=dataset_metadata
        )

class ForecastResult(Base):
    __tablename__ = 'forecast_results'
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, index=True)
    metric_name = Column(String(255), nullable=False)
    method = Column(String(100), nullable=False)
    forecast_data = Column(Text)
    confidence_level = Column(String(50))
    r2_score = Column(Float)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        if self.forecast_data:
            return json.loads(self.forecast_data)
        return None

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    metric_name = Column(String(255), nullable=False)
    condition_type = Column(String(50))
    threshold_value = Column(Float)
    email_recipients = Column(Text)
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime)
    trigger_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalyticsResult(Base):
    __tablename__ = 'analytics_results'
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, index=True)
    analysis_type = Column(String(100), nullable=False)
    result_data = Column(Text)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        if self.result_data:
            return json.loads(self.result_data)
        return None

class DataConnection(Base):
    __tablename__ = 'data_connections'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    connection_type = Column(String(50))
    connection_config = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def close_db():
    SessionLocal.remove()
