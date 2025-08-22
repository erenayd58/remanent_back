from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Remanent Backend"
    # SQLite ile başla; çok kullanıcılı ortamda PostgreSQL'e çevirebilirsin
    DATABASE_URL: str = "sqlite:///./remanent.db"
    LABEL_OUTPUT_DIR: str = "./labels"

    # Eşikler
    MIN_SHORT_EDGE_MM: int = 200
    MIN_AREA_M2: float = 0.06
    TOLERANCE_MM: int = 5

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
