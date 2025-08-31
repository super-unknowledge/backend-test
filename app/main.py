from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from pydantic import BaseModel
from app.db_connection import (
	get_db_session,
	get_engine
)
from typing import Annotated
from app.operations import create_candidate


@asynccontextmanager
async def lifespan(app: FastAPI):
	engine = get_engine()
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
		yield
	await engine.dispose()


app = FastAPI(lifespan=lifespan)


class CandidateRequest(BaseModel):
	full_name: str | None
	email: str | None
	phone: str | None
	skills: list[str] | None
 
 
# @app.get("/candidates")
# def read_candidates(db: Session = Depends(get_db)):
# 	candidates = db.query(Candidate).all()
# 	return candidates
# 
# 
@app.post("/candidates", response_model=dict[str, int])
async def create_candidate_route(
	candidate: CandidateRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	candidate_id = await create_candidate(
		db_session,
		candidate.full_name,
		candidate.email,
		candidate.phone,
		candidate.skills,
	)
	return {"candidate_id": candidate_id}
 
 
# # @app.get("/candidates")
# # def read_candidates():
# # list all candidates with optional filter by skill
# 
# @app.get("/candidates/{candidate_id}")
# def read_candidate(
# 	candidate_id: int,
# 	db: Session = Depends(get_db),
# ):
# 	candidate = (
# 		db.query(Candidate).filter(
# 			Candidate.id == candidate_id
# 		).first()
# 	)
# 	if candidate is None:
# 		raise HTTPException(
# 			status_code=404,
# 			detail="Candidate not found"
# 		)
# 	
# 	return candidate
# 	
# 
# @app.put("/candidates/{candidate_id}")
# def update_candidate(
# 	candidate_id: int,
# 	candidate: CandidateBody,
# 	db: Session = Depends(get_db),
# ):
# 	db_candidate = (
# 		db.query(Candidate).filter(
# 			Candidate.id == candidate_id
# 		).first()
# 	)
# 	if db_candidate is None:
# 		raise HTTPException(
# 			status_code=404,
# 			detail="Candidate not found"
# 		)
# 	db_candidate.full_name = candidate.full_name
# 	db_candidate.email = candidate.email
# 	db.commit()
# 	db.refresh(db_candidate)
# 	return db_candidate
# 	
# 
# # @app.post("/candidates/{candidate_id}/applications")
# # def create_application():
# 
# 
# # @app.get("/candidates/{candidate_id}/applications")
# # def read_applications():
# 
# 
# # @app.patch("/applications/{application_id}")
# # def update_application():
# 
