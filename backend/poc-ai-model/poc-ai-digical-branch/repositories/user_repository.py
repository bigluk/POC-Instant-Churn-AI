from typing import List, Optional
from core.database import get_db_connection


class UserRepository:
    def __init__(self):
        self.conn = get_db_connection()

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM ISBD_USERS WHERE id = %s;", (user_id,))
            return cur.fetchone()

    def get_all_users(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM ISBD_USERS;")
            return cur.fetchall()

    def update_investment_propensity(self, user_id: str, propensity: float, inclined_to_invest: int):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE ISBD_USERS SET investment_propensity = %s, inclined_to_invest = %s WHERE id = %s",
                (propensity, inclined_to_invest, user_id)
            )
            self.conn.commit()