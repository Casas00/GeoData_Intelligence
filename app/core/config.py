from pathlib import Path 
from pydantic_settings import BaseSettings, SettingsConfigDict

#Project Root Directory
BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    #Application Settings
    app_name: str = 'GeoData Intelligence'
    app_version: str ="0.1.0"
    debug: bool = True

    #Database Settings
    db_host: str = 'localhost'
    db_port: int = 5432
    db_name: str = 'geodata_intelligence'
    db_user: str 
    db_password: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()