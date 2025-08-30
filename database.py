from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
	pass


class Candidate(Base):
	__tablename__ = "candidate"
	id: Mapped[int] = mapped_column(
		primary_key=True,
	)
	full_name: Mapped[str]
	email: Mapped[str]
# 	phone: Mapped[str]
# 	skills: Mapped[str]
# 	created_at: Mapped[str]


# class Application(Base):
# 	__taplename__ = "application"
# 	id: Mapped[int] = mapped_column(
# 		primary_key=True,
# 	)
# 	candidate_id: Mapped[str]
# 	job_title: Mapped[str]
# 	status: Mapped[str]
# 	applied_at: Mapped[str]


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
	autocommit=False, autoflush=False, bind=engine
)

