from pydantic import BaseSettings

class Settings(BaseSettings):
	database_url: str
	REDIS_HOST: str
	REDIS_PORT: int

	class Config:
		env_file = ".env"


settings = Settings()
