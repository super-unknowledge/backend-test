from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
	select,
	update,
)
from app.models import Candidate
from typing import Optional


class CandidateRepository:
	async def create_candidate(
		db_session: AsyncSession,
		candidate: Candidate,
	) -> int:
		async with db_session.begin():
			db_session.add(candidate)
			await db_session.flush()
			candidate_id = candidate.id
			await db_session.commit()

		return candidate_id


	async def get_candidates(
		db_session: AsyncSession,
		skill: Optional[str] = None,
		limit: int = 10,
		offset: int = 20,
	):
		query = select(Candidate)

		if skill:
			query = query.where(Candidate.skills.contains([skill]))

		query = query.offset(offset).limit(limit)

		async with db_session as session:
			candidates = await session.execute(query)
			return candidates.scalars().all()


	async def get_candidate_by_id(
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
		update_candidate_dict: dict,
	) -> bool:
		candidate_query = update(Candidate).where(
			Candidate.id == candidate_id
		)

		updating_candidate_values = update_candidate_dict.copy()

		if updating_candidate_values == {}:
			return False

		candidate_query = candidate_query.values(
			**updating_candidate_values
		)

		async with db_session as session:
			result = await session.execute(candidate_query)
			await session.commit()
			if result.rowcount == 0:
				return False
			
			return True

