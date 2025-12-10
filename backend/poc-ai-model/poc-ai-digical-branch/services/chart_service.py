from typing import List, Dict
from repositories.propensity_repository import PropensityRepository


class ChartService:
    def __init__(self):
        self.propensity_repo = PropensityRepository()

    def get_user_propensity_chart(self, user_id: str) -> List[Dict]:
        rows = self.propensity_repo.get_user_propensity_history(user_id)

        if not rows:
            return None

        return [
            {
                "date": row["timestamp"].strftime("%d-%m-%Y"),
                "ip": float(row["investment_propensity"])
            }
            for row in rows
        ]