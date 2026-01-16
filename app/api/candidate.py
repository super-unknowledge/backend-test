#app/api/candidate.py
from fastapi import APIRouter
from app.models.candidate import CandidateBase, Candidate, CandidatePublic, CandidateCreate, CandidateUpdate
from app.models.application import ApplicationBase, Application, ApplicationPublic, ApplicationCreate
import app.mock.candidate as candidate_service
import app.mock.application as application_service


router = APIRouter(prefix = "/candidates")

@router.post("/")
async def create_candidate(candidate: CandidateCreate):
    return {"test create candidate"}

@router.post("/{candidate_id}/applications")
async def create_application():
    return {"test create candidate application"}

@router.get("/")
async def read_candidates():
    return {"test read candidates"}

@router.get("/{candidate_id}/applications")
async def read_applications():
    return {"test read candidate applications"}

@router.get("/{candidate_id}")
async def read_candidate():
    return {"test read candidate"}

@router.put("/{candidate_id}")
async def update_candidate():
    return {"test update candidate"}


