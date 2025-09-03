from sqlalchemy.orm import Session
from models import User
from email_validator import (
	validate_email,
	EmailNotValidError,
)
from operations import pwd_context

def authenticate_user(
	session: Session,
	email: str,
	password: str,
) -> User | None:
	try:
		validate_email(email)
		query_filter = User.email
	except EmailNotValidError:
		query_filter = User.username
	user = (
		session.query(User)
		.filter(query_filter == email)
		.first()
	)
	if not user or not pwd_context.verify(
		password, user.hashed_password
	):
		return
	return user
