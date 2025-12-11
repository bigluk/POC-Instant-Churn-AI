from typing import Optional, List, Dict
from core.database import get_db_connection


class PropensityRepository:
    def __init__(self):
        self.conn = get_db_connection()

    def get_latest_propensity_entry(self, user_id: str) -> Optional[Dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT timestamp
                FROM INVESTMENT_PROPENSITY_USER
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (user_id,)
            )
            return cur.fetchone()

    def add_propensity_entry(self, user_id: str, propensity: float, inclined_to_invest: int):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO INVESTMENT_PROPENSITY_USER 
                (user_id, investment_propensity, inclined_to_invest)
                VALUES (%s, %s, %s)
                """,
                (user_id, propensity, inclined_to_invest)
            )
            self.conn.commit()

    def get_user_propensity_history(self, user_id: str) -> List[Dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT investment_propensity, inclined_to_invest, timestamp
                FROM INVESTMENT_PROPENSITY_USER
                WHERE user_id = %s
                ORDER BY timestamp ASC
                """,
                (user_id,)
            )
            return cur.fetchall()