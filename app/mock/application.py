#app/mock/application.py
from app.models.application import ApplicationBase, Application, ApplicationPublic, ApplicationCreate, ApplicationUpdate


def update_application_status():
    return {"application status updated"}
