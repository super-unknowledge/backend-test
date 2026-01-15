#app/api/application.py
from fastapi import APIRouter


router = APIRouter(prefix = "/applications")

@router.patch("/{application_id}")
async def update_application_status():
    return {"test update application status"}
