from pydantic import (
	BaseModel,
	EmailStr,
)
from uuid import UUID

class CandidateRequest(BaseModel):
	id: UUID
	full_name: str
	email: EmailStr
	phone: str | None
	skills: list[str]
