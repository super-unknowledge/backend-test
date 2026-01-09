#app/api/candidate.py
from fastapi import APIRouter


router = APIRouter(prefix = "/candidates")

@router.post("/")
async def create_candidate():
    return {"test"}
