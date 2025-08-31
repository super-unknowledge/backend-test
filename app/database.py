from sqlalchemy import (
	ForeignKey,
	JSON,
	DateTime,
	Enum,
)
from sqlalchemy.orm import (
	DeclarativeBase, 
	Mapped, 
	mapped_column, 
	relationship
)
from datetime import datetime
import enum
from typing import List


class StatusEnum(enum.Enum):
	APPLIED = "APPLIED"
	INTERVIEWING = "INTERVIEWING"
	REJECTED = "REJECTED"
	HIRED = "HIRED"


class Base(DeclarativeBase):
	pass


class Candidate(Base):
	__tablename__ = "candidates"
	id: Mapped[int] = mapped_column(
		primary_key=True,
	)
	full_name: Mapped[str]
	email: Mapped[str] = mapped_column(
		unique=True,
	)
	phone: Mapped[str | None]
	skills: Mapped[list[str]] = mapped_column(JSON)
	created_at: Mapped[datetime] = mapped_column(
		DateTime, default=datetime.utcnow
	)
	applications: Mapped[list["Application"]] = relationship(
		back_populates="candidate"
	)


class Application(Base):
	__tablename__ = "applications"
	id: Mapped[int] = mapped_column(
		primary_key=True,
	)
	candidate_id: Mapped[int] = mapped_column(
		ForeignKey("candidates.id")
	)
	candidate: Mapped["Candidate"] = relationship(
		back_populates="applications"
	)
	job_title: Mapped[str]
	status: Mapped[StatusEnum] = mapped_column(
		Enum(StatusEnum, name="status_enum"),
		nullable=False,
		default=StatusEnum.APPLIED
	)
	applied_at: Mapped[datetime] = mapped_column(
		DateTime, default=datetime.utcnow
	)

