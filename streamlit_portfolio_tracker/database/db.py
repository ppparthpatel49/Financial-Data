import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Robust Path Configuration ---

# Define the project's base directory (the parent of the 'database' directory)
# This makes all paths relative to the project root, not the current working directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the .env file
env_path = BASE_DIR / '.env'

# Path to the data directory
data_dir = BASE_DIR / 'data'
os.makedirs(data_dir, exist_ok=True) # Ensure data directory exists

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Get DATABASE_URL from environment or fall back to a default absolute path
default_db_path = data_dir / 'portfolio.db'
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{default_db_path.as_posix()}")

# --- End Robust Path Configuration ---

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Provides a database session to the application."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()