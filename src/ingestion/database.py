import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.intelligence_report import Base
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("WARNING: DATABASE_URL not found in .env, falling back to localhost")
    DATABASE_URL = "postgresql://user:password@localhost:5432/signal_db"

engine  = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print(f"Database initialised at: {DATABASE_URL.split('@')[-1]}")

if __name__ == "__main__":
    init_db()