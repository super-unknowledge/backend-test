from sqlalchemy.ext.asyncio import create_async_engine

SQLALCHEMY_DATABASE_URL = (
	"sqlite+aiosqlite:///.database.db"
)


def get_engine():
	return create_async_engine(
		SQLALCHEMY_DATABASE_URL, echo=True
	)

