from typing import Annotated
import uuid
from datetime import datetime, timezone
import enum

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Column, JSON, Session, SQLModel, create_engine, select
from sqlalchemy import Enum as SQLEnum


class Status(str, enum.Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    REJECTED = "Rejected"
    HIRED = "Hired"


class CandidateBase(SQLModel):
    full_name: str
    email: str = Field(unique=True)
    phone: str | None = None
    skills: list[str] = Field(sa_column=Column(JSON))


class Candidate(CandidateBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc),
            nullable=False
    )

    applications: list["Application"] = Relationship(back_populates="candidate")


class CandidatePublic(CandidateBase):
    id: uuid.UUID


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    pass


class ApplicationBase(SQLModel):
    job_title: str
    status: Status = Field(sa_column=Column(SQLEnum(Status), default=Status.APPLIED))


class Application(ApplicationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    applied_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc),
            nullable=False
    )

    candidate_id: uuid.UUID = Field(foreign_key="candidate.id", nullable=False)
    candidate: Candidate | None = Relationship(back_populates="applications")


class ApplicationPublic(ApplicationBase):
    id: uuid.UUID
    candidate_id: uuid.UUID


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    status: Status = Status.APPLIED


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/candidates/", response_model=CandidatePublic)
def create_candidate(candidate: CandidateCreate, session: SessionDep):
    db_candidate = Candidate.model_validate(candidate)
    session.add(db_candidate)
    session.commit()
    session.refresh(db_candidate)
    return db_candidate


@app.post("/candidates/{candidate_id}/applications", response_model=ApplicationPublic)
def create_application(
        candidate_id: uuid.UUID,
        application: ApplicationCreate,
        session: SessionDep
):
    application_data = application.model_dump()
    db_application = Application(**application_data, candidate_id=candidate_id)
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application


@app.get("/candidates/", response_model=list[CandidatePublic])
def read_candidates(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    candidates = session.exec(select(Candidate).offset(offset).limit(limit)).all()
    return candidates


@app.get(
    "/candidates/{candidate_id}/applications",
    response_model=list[ApplicationPublic]
)
def read_applications(
    candidate_id: uuid.UUID,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    statement = (
        select(Application)
        .where(Application.candidate_id == candidate_id)
        .offset(offset)
        .limit(limit)
    )
    applications = session.exec(statement).all()

    return applications


@app.get("/candidates/{candidate_id}", response_model=CandidatePublic)
def read_candidate(candidate_id: uuid.UUID, session: SessionDep):
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.put("/candidates/{candidate_id}", response_model=CandidatePublic)
def update_candidate(
        candidate_id: uuid.UUID,
        candidate: CandidateUpdate,
        session: SessionDep
):
    candidate_db = session.get(Candidate, candidate_id)
    if not candidate_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate_data = candidate.model_dump()
    candidate_db.sqlmodel_update(candidate_data)
    session.add(candidate_db)
    session.commit()
    session.refresh(candidate_db)
    return candidate_db


@app.patch("/applications/{application_id}", response_model=ApplicationPublic)
def update_application_status(
    application_id: uuid.UUID,
    application: ApplicationUpdate,
    session: SessionDep
):
    application_db = session.get(Application, application_id)
    if not application_db:
        raise HTTPException(status_code=404, detail="Application not found")
    application_data = application.model_dump(exclude_unset=True)
    application_db.sqlmodel_update(application_data)
    session.add(application_db)
    session.commit()
    session.refresh(application_db)
    return application_db
