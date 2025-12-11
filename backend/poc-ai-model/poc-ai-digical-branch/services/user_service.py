from typing import List, Dict, Optional

from repositories.propensity_repository import PropensityRepository
from repositories.user_repository import UserRepository
from services.prediction_service import PredictionService


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.propensity_repo = PropensityRepository()
        self.prediction_service = PredictionService()

    def get_user(self, user_id: str) -> Optional[Dict]:
        return self.user_repo.get_user_by_id(user_id)

    def get_all_users(self) -> List[Dict]:
        return self.user_repo.get_all_users()

    def update_user_propensity(self, user_id: str, propensity: float):
        self.user_repo.update_investment_propensity(user_id, propensity)
        self.propensity_repo.add_propensity_entry(user_id, propensity)
