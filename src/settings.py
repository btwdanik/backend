from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    db_user: str = None
    db_password: str = None
    db_name: str = None
    db_host: str = "localhost"
    db_port: int = 5432

    model_config = {
        "env_file": BASE_DIR / "build" / ".env",
        "env_file_encoding": "utf-8",
    }