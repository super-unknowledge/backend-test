from pydantic import BaseModel


class CandidateRequest(BaseModel):
	full_name: str
	email: str
	phone: str | None
	skills: list[str]
