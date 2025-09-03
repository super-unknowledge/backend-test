from pydantic import BaseModel

from app.models.enums import StatusEnum


class ApplicationRequest(BaseModel):
	candidate_id: int
	job_title: str
	status: StatusEnum = StatusEnum.APPLIED


class ApplicationUpdateRequest(BaseModel):
	status: StatusEnum
