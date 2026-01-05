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


class Application(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    job_title: str
    status: Status = Field(sa_column=Column(SQLEnum(Status), default=Status.APPLIED))
    applied_at: datetime = Field(default_factory=datetime.now(timezone.utc), nullable=False)

    candidate_id: uuid.UUID | None = Field(default=None, foreign_key="candidate.id")
    candidate: Candidate | None = Relationship(back_populates="applications")


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


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


#@app.post("/candidates/{candidate_id}/applications")
#def create_application():


@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/candidates/", response_model=list[CandidatePublic])
def read_candidates(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    candidates = session.exec(select(Candidate).offset(offset).limit(limit)).all()
    return candidates


#@app.get("/candidates/{candidate_id}/applications")
#def read_applications():


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/candidates/{candidate_id}", response_model=CandidatePublic)
def read_candidate(candidate_id: uuid.UUID, session: SessionDep):
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


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


#@app.patch("/applications/{application_id}")
#def update_application_status()


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
