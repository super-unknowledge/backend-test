from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional

from app.db.session import get_db_session
from app.schemas.candidate import CandidateRequest
from app.services.candidate_service import CandidateService


router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/", response_model=dict[str, int])
async def create_candidate_route(
	candidate: CandidateRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	candidate_id = await CandidateService.create_candidate(
		db_session,
		candidate.full_name,  # TODO: refactor later full_name=...
		candidate.email,
		candidate.phone,
		candidate.skills,
	)
	return {"candidate_id": candidate_id}
 
 
@router.get("/")
async def get_candidates_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	skill: Optional[str] = None,
):
	return await CandidateService.get_candidates(db_session, skill)


@router.get("/{candidate_id}")
async def get_candidate_by_id_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	candidate_id: int,
):
	candidate = await CandidateService.get_candidate_by_id(db_session, candidate_id)
	if candidate is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	
	return candidate


@router.put("/{candidate_id}")
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

	updated = await CandidateService.update_candidate(
		db_session, candidate_id, update_dict_args
	)
	if not updated:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	return {"detail": "Candidate updated"}
