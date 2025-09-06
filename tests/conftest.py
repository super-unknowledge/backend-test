import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import AsyncMock

from app.main import app
from app.db.session import get_db_session

# Mocked async DB session
@pytest.fixture
def mock_db_session():
    return AsyncMock()

# Override the get_db_session dependency
@pytest.fixture
def override_get_db(mock_db_session):
    async def _get_mock_db():
        yield mock_db_session

    app.dependency_overrides[get_db_session] = _get_mock_db
    yield
    app.dependency_overrides.clear()

# Client using httpx.AsyncClient with ASGITransport
@pytest.fixture
async def client(override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
