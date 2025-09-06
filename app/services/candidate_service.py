from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.models import Candidate
from app.repositories.candidate_repository import CandidateRepository
from app.utils.redis import redis_client
import json


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
		skill: Optional[str] = None,
		limit: int = 10,
		offset: int = 20,
	):
		return await CandidateRepository.get_candidates(
		db_session=db_session,
		skill=skill,
		limit=limit,
		offset=offset,
		)


	async def get_candidate_by_id(
		db_session: AsyncSession,
		candidate_id: UUID,
	):
		return await CandidateRepository.get_candidate_by_id(db_session, candidate_id)


	async def update_candidate(
		db_session: AsyncSession,
		candidate_id: UUID,
		update_candidate_dict: dict,
	):
		return await CandidateRepository.update_candidate(db_session, candidate_id, update_candidate_dict)


	async def enqueue_candidate_task(candidate_id: UUID, task_type: str, metadata: dict = {}):
		task = {
			"candidate_id": candidate_id,
			"task_type": task_type,
			"metadata": metadata
		}
		await redis_client.rpush("candidate:processing_queue", json.dumps(task))


	async def process_candidate_task(task: dict):
		candidate_id = task["candidate_id"]
		task_type = task["task_type"]
		metadata = task.get("metadata", {})

		# Simulate processing
		print(f"Processing {task_type} for candidate {candidate_id}")
		await asyncio.sleep(2)  # Simulated work
