from uuid import UUID
from fastapi import (
	APIRouter,
	Depends,
	HTTPException,
	Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional

from app.db.session import get_db_session
from app.schemas.application import (
	ApplicationRequest,
	ApplicationUpdateRequest,
	ApplicationResponse,
)
from app.services.application_service import ApplicationService
from app.models.enums import StatusEnum


router = APIRouter(tags=["Applications"])

@router.post(
	"/candidates/{candidate_id}/applications",
	response_model=dict[str, UUID]
)
async def create_application_route(
	application: ApplicationRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	application_id = await ApplicationService.create_application(
		db_session,
		candidate_id=application.candidate_id,
		job_title=application.job_title,
		status=application.status,
	)
	return {"application_id": application_id}
 

@router.get(
	"/candidates/{candidate_id}/applications",
	response_model=List[ApplicationResponse]
)
async def get_applications_by_candidate_route(
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
	candidate_id: UUID,
	status: Optional[StatusEnum] = Query(
		None, description="Filter by application status"
	)
):
	applications =  await ApplicationService.get_applications_by_candidate(db_session, candidate_id, status=status)

	if not updated:
		raise HTTPException(
			status_code=404,
			detail="No applications found"
		)
	return applications


@router.patch("/applications/{application_id}")
async def update_application_status_route(
	application_id: UUID,
	application_update: ApplicationUpdateRequest,
	db_session: Annotated[
		AsyncSession, Depends(get_db_session)
	],
):
	updated = await ApplicationService.update_application_status(
		db_session, application_id, application_update.status
	)
	if not updated:
		raise HTTPException(
			status_code=404,
			detail="Application not found"
		)
	return {"detail": "Application updated"}
