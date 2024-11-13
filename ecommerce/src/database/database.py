from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

class DatabaseConnection:
    def __init__(self, database_url="sqlite:///ecommerce.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        Base.metadata.create_all(self.engine)
        
    def get_session(self):
        return self.SessionLocal()