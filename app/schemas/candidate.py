from pydantic import (
	BaseModel,
	EmailStr,
	Field,
)
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# request data for POST and PUT endpoints
class CandidateRequest(BaseModel):
	full_name: str = Field(
		example="Chris Martin"
	)
	email: EmailStr = Field(
		example="chris.martin@coldplay.com",
	)
	phone: Optional[str] = Field(
		None,
		example="(+63)2-8888-8888",
	)
	skills: list[str] = Field(
		example=["singing"],
	)


# request data for GET endpoints
class CandidateResponse(BaseModel):
	id: UUID = Field(
		example="123e4567-e89b-12d3-a456-426614174000",
	)
	full_name: str = Field(
		example="Chris Martin"
	)
	email: EmailStr = Field(
		example="chris.martin@coldplay.com",
	)
	phone: Optional[str] = Field(
		None,
		example="(+63)2-8888-8888",
	)
	skills: list[str] = Field(
		example=["singing"],
	)
	created_at: datetime = Field(
		example="2025-09-05T14:30:00Z",
	)

	class Config:
		orm_mode = True
