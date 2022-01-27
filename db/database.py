import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.environ.get("nsatr")
DB_PASSWORD = os.environ.get("Password1")
DB_NAME = os.environ.get("testserver-mysql.mysql.database.azure.com")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_NAME}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./nstar.db"

newengine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=newengine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()