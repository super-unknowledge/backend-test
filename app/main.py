from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from pydantic import BaseModel
from app.db_connection import (
	get_db_session,
	get_engine
)
from typing import Annotated
from app.operations import (
	create_candidate,
	create_application,
	get_candidates,
	get_candidate,
	get_applications,
	update_candidate,
	update_application_status,
)
from app.database import StatusEnum  # Expose seperately later
from typing import Optional
@asynccontextmanager
async def lifespan(app: FastAPI):
	engine = get_engine()
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
		yield
	await engine.dispose()


app = FastAPI(lifespan=lifespan)


class CandidateRequest(BaseModel):
	full_name: str | None
	email: str | None
	phone: str | None
	skills: list[str] | None
 
 
@app.post("/candidates", response_model=dict[str, int])
async def create_candidate_route(
	candidate: CandidateRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	candidate_id = await create_candidate(
		db_session,
		candidate.full_name,
		candidate.email,
		candidate.phone,
		candidate.skills,
	)
	return {"candidate_id": candidate_id}
 
 
@app.get("/candidates")
async def get_candidates_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	skill: Optional[str] = None,
):
	candidates = await get_candidates(db_session, skill)

	if candidates is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	
	return candidates

@app.get("/candidates/{candidate_id}")
async def get_candidate_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	candidate_id: int,
):
	candidate = await get_candidate(db_session, candidate_id)
	if candidate is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	
	return candidate


@app.put("/candidates/{candidate_id}")
async def update_candidate_route(
	candidate_id: int,
	candidate_update: CandidateRequest,
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
):
	update_dict_args = candidate_update.model_dump(
		exclude_unset=True
	)

	updated = await update_candidate(
		db_session, candidate_id, update_dict_args
	)
	if not updated:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	return {"detail": "Candidate updated"}
	

class ApplicationRequest(BaseModel):
	candidate_id: int
	job_title: str | None
	status: StatusEnum = StatusEnum.APPLIED
 
 
@app.post(
	"/candidates/{candidate_id}/applications",
	response_model=dict[str, int]
)
async def create_application_route(
	application: ApplicationRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	application_id = await create_application(
		db_session,
		candidate_id=application.candidate_id,
		job_title=application.job_title,
		status=application.status,
	)
	return {"application_id": application_id}
 

@app.get("/candidates/{candidate_id}/applications")
async def read_applications_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	candidate_id: int,
):
	applications = await get_applications(
		db_session,
		candidate_id
	)
	if applications is None:
		raise HTTPException(
			status_code=404,
			detail="Application not found"
		)
	
	return applications


class ApplicationUpdateRequest(BaseModel):
	status: StatusEnum


@app.patch("/applications/{application_id}")
async def update_application_status_route(
	application_id: int,
	application_update: ApplicationUpdateRequest,
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
):
	updated = await update_application_status(
		db_session, application_id, application_update.status
	)
	if not updated:
		raise HTTPException(
			status_code=404,
			detail="Application not found"
		)
	return {"detail": "Application updated"}
	
