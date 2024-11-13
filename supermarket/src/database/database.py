from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

class DatabaseConnection:
    def __init__(self, database_url="sqlite:///supermarket.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """提供基本的 session 創建"""
        return self.SessionLocal()
    
    def _create_tables(self):
        """私有方法：創建資料表"""
        Base.metadata.create_all(self.engine)
    
    def _delete_tables(self):
        """私有方法：刪除資料表"""
        Base.metadata.drop_all(self.engine)