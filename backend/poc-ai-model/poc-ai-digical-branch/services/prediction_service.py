from typing import List, Tuple

from ml.model_loader import ModelLoader
from ml.preprocessor import DataPreprocessor


class PredictionService:
    def __init__(self):
        self.model_loader = ModelLoader.get_instance()
        self.preprocessor = DataPreprocessor()

    def predict_single(self, data: dict) -> Tuple[int, List[float], float]:
        X = self.preprocessor.prepare_input(data)
        model = self.model_loader.model

        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        pred_proba = proba[pred]

        return int(pred), proba.tolist(), float(pred_proba)

    def predict_batch(self, users: List[dict]) -> List[Tuple[int, List[float], float]]:
        X = self.preprocessor.prepare_batch(users)
        model = self.model_loader.model

        preds = model.predict(X)
        probas = model.predict_proba(X)

        results = []
        for pred, proba_vector in zip(preds, probas):
            pred_proba = proba_vector[pred]
            results.append((int(pred), proba_vector.tolist(), float(pred_proba)))

        return results
