from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "lovable Backend API"
    VERSION: str = "v1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()

