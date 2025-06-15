import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db():
    """Create a test database connection."""
    # Use a test database
    settings.DATABASE_NAME = f"{settings.DATABASE_NAME}_test"
    
    # Connect to the test database
    await connect_to_mongo()
    
    yield
    
    # Clean up after tests
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await client.drop_database(settings.DATABASE_NAME)
    await close_mongo_connection()

@pytest.fixture
async def clean_db(test_db):
    """Clean the database before each test."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await client[settings.DATABASE_NAME].verifications.delete_many({})
    yield
    await client[settings.DATABASE_NAME].verifications.delete_many({}) 