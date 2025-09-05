from pydantic import BaseModel
from uuid import UUID

from app.models.enums import StatusEnum


class ApplicationRequest(BaseModel):
	id: UUID
	candidate_id: UUID
	job_title: str
	status: StatusEnum = StatusEnum.APPLIED


class ApplicationUpdateRequest(BaseModel):
	status: StatusEnum
