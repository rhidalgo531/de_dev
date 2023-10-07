from pydantic_settings import BaseSettings, EnvSettingsSource
import os 

class PostgresSettings(EnvSettingsSource):
    FASTAPI_DB_USER: str  
    FASTAPI_DB_PASSWORD: str  
    POSTGRES_DB: str  
    POSTGRES_HOST: str 


class Settings(BaseSettings):
    app_name: str = "Computer Metrics API"


settings = Settings()