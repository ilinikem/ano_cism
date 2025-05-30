from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import send_task
from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
AsyncSessionTest = sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session")
async def async_engine():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine_test
    await engine_test.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine):
    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture(autouse=True)
def mock_send_task_to_queue(monkeypatch):
    monkeypatch.setattr(send_task, "send_task_to_queue", AsyncMock())
