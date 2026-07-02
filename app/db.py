import os
from sqlalchemy import create_engine

USERS_DB_URL = os.getenv("DATABASE_USERS_URL")
DATA_DB_URL = os.getenv("DATABASE_DATA_URL")

users_engine = create_engine(USERS_DB_URL, pool_pre_ping=True)
data_engine = create_engine(DATA_DB_URL, pool_pre_ping=True)