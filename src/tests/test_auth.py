from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import database_url, Base, get_db

engine = create_engine(
    database_url
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register():
    data = {
        'username': 'renren-017',
        'password': 'secretpass123'
    }
    response = client.post('/auth/register/', json=data)
    assert response.status_code == 200
