from contextlib import contextmanager
from .database import DatabaseConnection

class DatabaseManager:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def initialize_database(self):
        """初始化資料庫"""
        try:
            self.db._create_tables()
        except Exception as e:
            raise Exception(f"初始化資料庫失敗：{str(e)}")
    
    def reset_database(self):
        """重置資料庫"""
        try:
            self.db._delete_tables()
            self.db._create_tables()
        except Exception as e:
            raise Exception(f"重置資料庫失敗：{str(e)}")
    
    @contextmanager
    def get_db_session(self):
        """提供一個安全的 session 上下文管理器"""
        session = self.db.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"資料庫操作失敗：{str(e)}")
        finally:
            session.close()
    
    def execute_transaction(self, operation):
        """執行資料庫交易"""
        with self.get_db_session() as session:
            return operation(session)