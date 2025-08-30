from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, Candidate

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


app = FastAPI()

@app.get("/")
def read_root():
	return ("root")

@app.get("/candidates")
def read_candidates(db: Session = Depends(get_db)):
	candidates = db.query(Candidate).all()
	return candidates
