import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import asyncpg

from app.db.engine import get_engine
from app.db.base import Base
from app.api import candidate_routes, application_routes

from app.models.candidate import Candidate
from app.models.application import Application

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def wait_for_db(engine, retries=10, delay=2):
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("Database is ready.")
            return
        except (OperationalError, asyncpg.exceptions.CannotConnectNowError, ConnectionRefusedError) as e:
            print(f"DB not ready yet (attempt {attempt}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("Database connection failed after retries.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    await wait_for_db(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Include API routers
app.include_router(candidate_routes.router)
app.include_router(application_routes.router)
