from sqlalchemy import (
	ForeignKey,
	DateTime,
	Enum,
)
from sqlalchemy.orm import (
	Mapped, 
	mapped_column, 
	relationship
)
from datetime import datetime

from app.db.base import Base
from app.models.enums import StatusEnum

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
