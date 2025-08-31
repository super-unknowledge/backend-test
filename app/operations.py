from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Candidate, Application


async def create_candidate(
	db_session: AsyncSession,
	full_name: str,
	email: str,
	phone: str = None,
	skills: list[str] = None,
) -> int:
	candidate = Candidate(
		full_name=full_name,
		email=email,
		phone=phone,
		skills=skills
	)

	async with db_session.begin():
		db_session.add(candidate)
		await db_session.flush()
		candidate_id = candidate.id
		await db_session.commit()
	return candidate_id


async def get_candidates(
	db_session: AsyncSession,
):
	query = (
		select(Candidate)
	)

	async with db_session as session:
		candidates = await session.execute(query)
		return candidates.scalars().all()


async def get_candidate(
	db_session: AsyncSession,
	candidate_id: int,
) -> Candidate | None:
	query = (
		select(Candidate)
		.where(Candidate.id == candidate_id)
	)

	async with db_session as session:
		candidate = await session.execute(query)
		return candidate.scalars().first()


async def update_candidate(
	db_session: AsyncSession,
	candidate_id: int,
	new_full_name: str = None,
	new_email: str = None,
	new_phone: str = None,
	new_skills: list[str] = None,
) -> bool:
	query = (
		update(Candidate)
		.where(Candidate.id == candidate_id)
		.values(
			full_name=new_full_name,
			email=new_email,
			phone=new_phone,
			skills=new_skills
		)
	)

	async with db_session as session:
		candidate_updated = await session.execute(query)
		await session.commit()
		if candidate_updated.rowcount == 0:
			return False
		return True


# async def create_application():
# 
# 
# async def get_applications():
# 
# 
# async def update_application_status():
