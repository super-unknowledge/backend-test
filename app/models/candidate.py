import uuid
from sqlalchemy import (
	JSON,
	DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
	Mapped, 
	mapped_column, 
	relationship
)
from datetime import datetime
from app.db.base import Base

class Candidate(Base):
	__tablename__ = "candidates"
	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		primary_key=True,
		default=uuid.uuid4,
		index=True
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
