import os
import pytest
from fastapi.testclient import TestClient

# ensure test DB
os.environ["DATABASE_URL"] = "sqlite:///./test_database.db"
os.environ["SECRET_KEY"] = "testsecret"
os.environ["ADMIN_SECRET"] = "testadminsecret"

from app.main import app
from app.database import create_db_and_tables, engine
from sqlmodel import SQLModel

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # create fresh test DB
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()
    yield
    # teardown
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def client():
    return TestClient(app)
