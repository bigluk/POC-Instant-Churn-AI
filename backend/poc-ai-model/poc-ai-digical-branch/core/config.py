from pydantic_settings import BaseSettings
from pydantic import Field
import os


def get_model_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # .../core/
    project_dir = os.path.dirname(current_dir)  # .../poc-ai-digical-branch/
    base_project = os.path.dirname(project_dir)  # .../poc-ai-model/

    return os.path.join(
        base_project,
        "ml_algorithms",
        "ml_xgboost",
        "xg-boost-model.pkl"
    )


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "poc_isbd"
    db_user: str = "isbd"
    db_password: str = "isbd"

    model_path: str = Field(default_factory=get_model_path)

    class Config:
        env_file = ".env"


settings = Settings()
print(f"Model will be loaded from: {settings.model_path}")
