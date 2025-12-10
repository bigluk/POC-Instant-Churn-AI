import pandas as pd
from typing import List
from core.utils import prepare_sample

DF_COLUMNS = ["age", "job", "marital", "education", "default",
              "balance", "housing", "loan"]


class DataPreprocessor:
    @staticmethod
    def prepare_input(data: dict) -> pd.DataFrame:
        df = pd.DataFrame([data], columns=DF_COLUMNS)
        return prepare_sample(df)

    @staticmethod
    def prepare_batch(users: List[dict]) -> pd.DataFrame:
        rows = [
            [
                u['age'],
                u['job'],
                u['marital'],
                u['education'],
                u['default_status'],
                int(u['balance']),
                u['housing'],
                u['loan']
            ]
            for u in users
        ]
        df = pd.DataFrame(rows, columns=DF_COLUMNS)
        return prepare_sample(df)