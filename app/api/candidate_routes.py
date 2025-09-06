from uuid import UUID
from fastapi import (
	APIRouter,
	Depends,
	HTTPException,
	Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional, List

from app.db.session import get_db_session
from app.schemas.candidate import CandidateRequest, CandidateResponse
from app.services.candidate_service import CandidateService


router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/", response_model=dict[str, UUID])
async def create_candidate_route(
	candidate: CandidateRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	candidate_id = await CandidateService.create_candidate(
		db_session,
		full_name=candidate.full_name,
		email=candidate.email,
		phone=candidate.phone,
		skills=candidate.skills,
	)
	return {"candidate_id": candidate_id}
 
 
@router.get("/", response_model=List[CandidateResponse])
async def get_candidates_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	skill: Optional[str] = None,
	limit: int = Query(10, ge=1),
	offset: int = Query(20, ge=0),
):
	candidates =  await CandidateService.get_candidates(db_session, skill)
	
	if candidates is None:
		raise HTTPException(
			status_code=404,
			detail="No candidates found"
		)
	
	return candidates


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate_by_id_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	candidate_id: UUID,
):
	candidate = await CandidateService.get_candidate_by_id(db_session, candidate_id)

	if candidate is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	
	return candidate


@router.put("/{candidate_id}", response_model=dict[str, str])
async def update_candidate_route(
	candidate_id: UUID,
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
