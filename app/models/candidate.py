import uuid
from datetime import datetime, timezone

from sqlmodel import Field, Column, JSON, SQLModel, Relationship


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

