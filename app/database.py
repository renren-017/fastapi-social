from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


engine = create_engine(
    os.environ['DATABASE_URL']
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        print(type(db))
        yield db
    finally:
        db.close()


def add_to_db(db: Session = Depends(get_db), *objects):
    for obj in objects:
        db.add(obj)
        db.commit()
