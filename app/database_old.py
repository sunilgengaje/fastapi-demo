# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# Use percent-encoded password in the URL if it contains special chars
DATABASE_URL = "mysql+pymysql://root:Root%40123@127.0.0.1:3306/fastapi_demo"

# Engine creation
engine = create_engine(
    DATABASE_URL,
    echo=True,         # set to False in production
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative class
Base = declarative_base()

def get_engine():
    """
    Return the SQLAlchemy engine. Useful when other modules need direct access.
    """
    return engine

def init_db(create_tables: bool = True):
    """
    Initialize DB connection and (optionally) create tables.

    - create_tables=True will call Base.metadata.create_all(bind=engine)
      to create any missing tables from your models.
    - This function centralizes DB initialization so other modules can import it.
    """
    try:
        # simple test connection
        conn = engine.connect()
        conn.close()
    except OperationalError as e:
        # Re-raise with clearer message for development
        raise OperationalError(
            f"Could not connect to the database. Check DATABASE_URL and that MySQL is running.\nOriginal error: {e}"
        ) from e

    if create_tables:
        # Import models here (deferred) so all model modules are loaded before create_all
        # Example: from . import models  # ensures models are registered with Base
        Base.metadata.create_all(bind=engine)
