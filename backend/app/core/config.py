from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "lovable Backend API"
    VERSION: str = "v1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()

