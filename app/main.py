from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.engine import get_engine
from app.db.base import Base

from app.api import candidate_routes, application_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
	engine = get_engine()
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
		yield
	await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Include API routers
app.include_router(candidate_routes.router)
app.include_router(application_routes.router)

