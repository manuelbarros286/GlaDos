from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.intelligence_report import Base

DATABASE_URL = "postgresql://user:password@localhost:5432/signal_db"
engine  = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print(f"Database initialised!")

if __name__ == "__main__":
    init_db()