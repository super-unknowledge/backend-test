from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from app.models.enums import StatusEnum


class ApplicationRequest(BaseModel):
	candidate_id: UUID = Field(
		example="123e4567-e89b-12d3-a456-426614174000",
	)
	job_title: str = Field(
		example="Lead Singer",
	)
	status: StatusEnum = Field(
		StatusEnum.APPLIED,
		example="APPLIED",
	)


class ApplicationUpdateRequest(BaseModel):
	status: StatusEnum = Field(
		example="HIRED",
	)


class ApplicationResponse(BaseModel):
	id: UUID
	candidate_id: UUID = Field(
		example="123e4567-e89b-12d3-a456-426614174000",
	)
	job_title: str = Field(
		example="Lead Singer",
	)
	status: StatusEnum = Field(
		StatusEnum.APPLIED,
		example="APPLIED",
	)
	applied_at: datetime = Field(
		example="2025-09-05T14:30:00Z",
	)
