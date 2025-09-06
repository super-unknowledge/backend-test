from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
	select,
	update,
)
from typing import Optional

from app.models import Application
from app.models.enums import StatusEnum


class ApplicationRepository:
	async def create_application(
		db_session: AsyncSession,
		application: Application,
	) -> int:
		async with db_session.begin():
			db_session.add(application)
			await db_session.flush()
			application_id = application.id
			await db_session.commit()
		return application_id


	async def get_applications_by_candidate(
		db_session: AsyncSession,
		candidate_id: int,
		status: Optional[StatusEnum] = None
	) -> list[Application]:
		query = (
			select(Application)
			.where(Application.candidate_id == candidate_id)
		)

		if status:
			query = query.where(Application.status == status)

		async with db_session as session:
			applications = await session.execute(query)
			return applications.scalars().all()


	async def update_application_status(
		db_session: AsyncSession,
		application_id: int,
		new_status: StatusEnum,
	) -> bool:
		query = (
			update(Application)
			.where(Application.id == application_id)
			.values(status=new_status)
		)
		async with db_session as session:
			application_updated = await session.execute(query)
			await session.commit()
			if application_updated.rowcount == 0:
				return False
			return True

