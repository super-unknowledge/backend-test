from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import Application
from app.models.enums import StatusEnum
from app.repositories import ApplicationRepository


class ApplicationService:
	async def create_application(
		db_session: AsyncSession,
		candidate_id: UUID,
		job_title: str,
		status: StatusEnum = StatusEnum.APPLIED,
	):
		application = Application(
			candidate_id=candidate_id,
			job_title=job_title,
			status=status,
		)

		return await ApplicationRepository.create_application(db_session, application)


	async def get_applications_by_candidate(
		db_session: AsyncSession,
		candidate_id: UUID,
		status: Optional[StatusEnum] = None
	):
		return await ApplicationRepository.get_applications_by_candidate(
			db_session=db_session,
			candidate_id=candidate_id,
			status=status,
		)


	async def update_application_status(
		db_session: AsyncSession,
		application_id: UUID,
		new_status: StatusEnum,
	):
		return await ApplicationRepository.update_application_status(db_session, application_id, new_status)

