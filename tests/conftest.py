import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from common.database import Base, get_db
from user.main import app as user_app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="user_client")
def user_client_fixture(session: Session):
    def get_session_override():
        return session

    user_app.dependency_overrides[get_db] = get_session_override

    client = TestClient(user_app)
    yield client
    user_app.dependency_overrides.clear()
