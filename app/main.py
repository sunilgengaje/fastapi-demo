# app/main.py
from fastapi import FastAPI
from .controllers import router as item_router

# import models so they register with Base.metadata
from . import models

from .database import Base, engine, init_db

# create tables (init_db will call Base.metadata.create_all if implemented)
# If you have init_db in database.py, call it:
try:
    init_db(create_tables=True)
except Exception:
    # fallback to direct create_all if init_db not present or raises
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(item_router)
