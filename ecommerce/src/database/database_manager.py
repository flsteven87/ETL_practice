from .database import DatabaseConnection

class DatabaseManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.create_tables()
    
    def add_records(self, records):
        session = self.db.get_session()
        try:
            session.add_all(records)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()