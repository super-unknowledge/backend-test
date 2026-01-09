from typing import Annotated
import uuid
from datetime import datetime, timezone
import enum

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Column, JSON, Session, SQLModel, select
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.candidate import CandidateBase, Candidate, CandidatePublic, CandidateCreate, CandidateUpdate
from app.models.application import ApplicationBase, Application, ApplicationPublic, ApplicationCreate, ApplicationUpdate


sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.post("/candidates/", response_model=CandidatePublic)
async def create_candidate(candidate: CandidateCreate, session: AsyncSessionDep):
    db_candidate = Candidate.model_validate(candidate)
    session.add(db_candidate)
    await session.commit()
    await session.refresh(db_candidate)
    return db_candidate


@app.post("/candidates/{candidate_id}/applications", response_model=ApplicationPublic)
async def create_application(
    candidate_id: uuid.UUID,
    application: ApplicationCreate,
    session: AsyncSessionDep
):
    application_data = application.model_dump()
    db_application = Application(**application_data, candidate_id=candidate_id)
    session.add(db_application)
    await session.commit()
    await session.refresh(db_application)
    return db_application


@app.get("/candidates/", response_model=list[CandidatePublic])
async def read_candidates(
    session: AsyncSessionDep,
    limit: int = 10,
    offset: int = 20,
):
    result = await session.exec(select(Candidate).offset(offset).limit(limit))
    candidates = result.all()
    return candidates


@app.get(
    "/candidates/{candidate_id}/applications",
    response_model=list[ApplicationPublic]
)
async def read_applications(
    candidate_id: uuid.UUID,
    session: AsyncSessionDep,
):
    candidate = await session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    statement = (
        select(Application)
        .where(Application.candidate_id == candidate_id)
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(statement)
    applications = result.all()

    return applications


@app.get("/candidates/{candidate_id}", response_model=CandidatePublic)
async def read_candidate(candidate_id: uuid.UUID, session: AsyncSessionDep):
    candidate = await session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.put("/candidates/{candidate_id}", response_model=CandidatePublic)
async def update_candidate(
    candidate_id: uuid.UUID,
    candidate: CandidateUpdate,
    session: AsyncSessionDep
):
    candidate_db = await session.get(Candidate, candidate_id)
    if not candidate_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate_data = candidate.model_dump()
    candidate_db.sqlmodel_update(candidate_data)
    session.add(candidate_db)
    await session.commit()
    await session.refresh(candidate_db)
    return candidate_db


@app.patch("/applications/{application_id}", response_model=ApplicationPublic)
async def update_application_status(
    application_id: uuid.UUID,
    application: ApplicationUpdate,
    session: AsyncSessionDep
):
    application_db = await session.get(Application, application_id)
    if not application_db:
        raise HTTPException(status_code=404, detail="Application not found")
    application_data = application.model_dump(exclude_unset=True)
    application_db.sqlmodel_update(application_data)
    session.add(application_db)
    await session.commit()
    await session.refresh(application_db)
    return application_db
