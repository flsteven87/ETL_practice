from contextlib import contextmanager
from .database import DatabaseConnection

class DatabaseManager:
    def __init__(self):
        self.db= DatabaseConnection()

    def initialize_database(self):
        try:
            self.db._delete_tables()
            self.db._create_tables()
        except Exception as e:
            raise Exception(str(e))
        
    @contextmanager
    def get_db_session(self):

        session = self.db.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(str(e))
        finally:
            session.close()
    
    def execute_transaction(self, operation):
        with self.get_db_session() as session:
            return operation(session)
        
if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.initialize_database()