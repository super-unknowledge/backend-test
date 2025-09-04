from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings


def get_engine():
	return create_async_engine(
		settings.database_url, echo=True
	)

