from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from dotenv import load_dotenv
from decouple import AutoConfig, RepositoryEnv

config = AutoConfig(search_path='/fastapi-social')
database_url = 'postgresql://{}:{}@{}:{}/{}'.format(
        config('POSTGRES_USER'),
        config('POSTGRES_PASSWORD'),
        config('POSTGRES_HOST'),
        config('POSTGRES_PORT'),
        config('POSTGRES_DB')
    )
engine = create_engine(
    database_url
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_to_db(db: Session = Depends(get_db), *objects):
    for obj in objects:
        db.add(obj)
        db.commit()
