import joblib
from typing import Any
from core.config import settings


class ModelLoader:
    _instance = None

    @staticmethod
    def get_instance():
        if ModelLoader._instance is None:
            ModelLoader._instance = ModelLoader()
        return ModelLoader._instance

    def __init__(self):
        self._model = None

    def load_model(self):
        if self._model is None:
            self._model = joblib.load(settings.model_path)
        return self._model

    @property
    def model(self) -> Any:
        return self.load_model()
