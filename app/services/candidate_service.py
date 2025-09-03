from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import Candidate
from app.repositories.candidate_repository import CandidateRepository


class CandidateService:
	async def create_candidate(
		db_session: AsyncSession,
		full_name: str,
		email: str,
		phone: str = None,
		skills: list[str] = None,
	):
		candidate = Candidate(
			full_name=full_name,
			email=email,
			phone=phone,
			skills=skills
		)

		return await CandidateRepository.create_candidate(db_session, candidate)


	async def get_candidates(
		db_session: AsyncSession,
		skill: Optional[str] = None
	):
		return await CandidateRepository.get_candidates(db_session, skill)


	async def get_candidate_by_id(
		db_session: AsyncSession,
		candidate_id: int,
	):
		return await CandidateRepository.get_candidate_by_id(db_session, candidate_id)


	async def update_candidate(
		db_session: AsyncSession,
		candidate_id: int,
		update_candidate_dict: dict,
	):
		return await CandidateRepository.update_candidate(db_session, candidate_id, update_candidate_dict)

