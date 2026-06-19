import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database import get_session
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def disable_celery():
    import tasks.service as service
    def fake_delay(*args, **kwargs):
        return None
    if hasattr(service, "process_booking"):
        service.process_booking.delay = fake_delay


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    async def init():
        async with engine.begin() as conn:
            from bookings.models import Base
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init())


@pytest.fixture(scope="session", autouse=True)
def override_dependencies():
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac
