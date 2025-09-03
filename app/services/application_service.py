from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Application
from app.models.enums import StatusEnum
from app.repositories import ApplicationRepository


class ApplicationService:
	async def create_application(
		db_session: AsyncSession,
		candidate_id: int,
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
		candidate_id: int,
	):
		return await ApplicationRepository.get_applications_by_candidate(db_session, candidate_id)


	async def update_application_status(
		db_session: AsyncSession,
		application_id: int,
		new_status: StatusEnum,
	):
		return await ApplicationRepository.update_application_status(db_session, application_id, new_status)

