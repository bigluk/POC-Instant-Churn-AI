from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from repositories.user_repository import UserRepository
from repositories.propensity_repository import PropensityRepository
from services.prediction_service import PredictionService


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.propensity_repo = PropensityRepository()
        self.prediction_service = PredictionService()

    def get_enriched_user(self, user_id: str) -> Optional[Dict]:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return None
        return self._enrich_users_with_predictions([user])[0]

    def get_all_enriched_users(self) -> List[Dict]:
        users = self.user_repo.get_all_users()
        return self._enrich_users_with_predictions(users)

    def _enrich_users_with_predictions(self, users: List[Dict]) -> List[Dict]:
        if not users:
            return []

        predictions_data = self.prediction_service.predict_batch(users)

        enriched_users = []
        for user, (pred, probabilities, pred_proba) in zip(users, predictions_data):
            investment_propensity = round(float(probabilities[1]) * 100, 2)
            user['prediction'] = pred
            user['probabilities'] = probabilities
            user['investment_propensity'] = investment_propensity
            user['pred_proba'] = pred_proba

            should_update = self._should_update_propensity(user, investment_propensity)
            if should_update:
                self._update_user_propensity(user['id'], investment_propensity)
            enriched_users.append(user)

        return enriched_users

    def _should_update_propensity(self, user: Dict, new_propensity: float) -> bool:
        if user.get('investment_propensity') is None:
            return True
        last_entry = self.propensity_repo.get_latest_propensity_entry(user['id'])
        if last_entry is None:
            return True
        last_time = last_entry['timestamp']
        update_threshold = datetime.now(timezone.utc) - timedelta(days=1)

        return last_time < update_threshold

    def _update_user_propensity(self, user_id: str, propensity: float):
        self.user_repo.update_investment_propensity(user_id, propensity)
        self.propensity_repo.add_propensity_entry(user_id, propensity)
