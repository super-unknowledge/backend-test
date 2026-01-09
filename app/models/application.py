import uuid
from datetime import datetime, timezone
import enum

from sqlmodel import Field, Column, JSON, SQLModel, Relationship
from sqlalchemy import Enum as SQLEnum

from app.models.candidate import Candidate


class Status(str, enum.Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    REJECTED = "Rejected"
    HIRED = "Hired"


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
