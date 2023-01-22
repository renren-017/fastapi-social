import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import AutoConfig

from database import get_db, Base


config = AutoConfig(search_path='/fastapi-social')
engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format(
        config('POSTGRES_USER'),
        config('POSTGRES_PASSWORD'),
        config('POSTGRES_TESTING_HOST'),
        config('POSTGRES_PORT'),
        config('POSTGRES_DB')
    )
)


@pytest.fixture(scope='session')
def setup_database():
    Base.metadata.bind = engine
    Base.metadata.create_all()

    yield

    Base.metadata.drop_all()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
