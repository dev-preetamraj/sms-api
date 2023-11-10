from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from django.conf import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo = False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()
