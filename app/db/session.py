from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.engine import get_engine

AsyncSessionLocal = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=get_engine(),
	class_=AsyncSession,
)


async def get_db_session():
	async with AsyncSessionLocal() as session:
		yield session

