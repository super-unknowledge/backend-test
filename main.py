from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Candidate
from pydantic import BaseModel

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


app = FastAPI()

class CandidateBody(BaseModel):
	full_name: str
	email: str
	# phone: str
	# skills: str
	# created_at: str


@app.get("/candidates")
def read_candidates(db: Session = Depends(get_db)):
	candidates = db.query(Candidate).all()
	return candidates


@app.post("/candidates")
def create_candidate(
	candidate: CandidateBody,
	db: Session = Depends(get_db)
):
	new_candidate = Candidate(
		full_name=candidate.full_name,
		email=candidate.full_name
	)
	db.add(new_candidate)
	db.commit()
	db.refresh(new_candidate)
	return new_candidate


# @app.get("/candidates")
# def read_candidates():
# list all candidates with optional filter by skill

@app.get("/candidates/{candidate_id}")
def read_candidate(
	candidate_id: int,
	db: Session = Depends(get_db),
):
	candidate = (
		db.query(Candidate).filter(
			Candidate.id == candidate_id
		).first()
	)
	if candidate is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	
	return candidate
	

@app.put("/candidates/{candidate_id}")
def update_candidate(
	candidate_id: int,
	candidate: CandidateBody,
	db: Session = Depends(get_db),
):
	db_candidate = (
		db.query(Candidate).filter(
			Candidate.id == candidate_id
		).first()
	)
	if db_candidate is None:
		raise HTTPException(
			status_code=404,
			detail="Candidate not found"
		)
	db_candidate.full_name = candidate.full_name
	db_candidate.email = candidate.email
	db.commit()
	db.refresh(db_candidate)
	return db_candidate
	

# @app.post("/candidates/{candidate_id}/applications")
# def create_application():


# @app.get("/candidates/{candidate_id}/applications")
# def read_applications():


# @app.patch("/applications/{application_id}")
# def update_application():

