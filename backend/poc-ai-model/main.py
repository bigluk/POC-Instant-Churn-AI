import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI

from common_utils import prepare_sample
from models import ModelInput, User

app = FastAPI()

DF_COLUMNS = ["age", "job", "marital", "education", "default", "balance", "housing", "loan"]

# Load model
model = joblib.load("xgboost/xg-boost-model.pkl")


def load_users_from_file(path: str) -> dict[str, User]:
    file_path = Path(path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users_dict = {item["id"]: User(**item) for item in data}
    return users_dict


users_db = load_users_from_file("data/test_users_db.json")


@app.post("/api/predict")
async def predict(data: ModelInput):
    test_input = [
        data.age,
        data.job,
        data.marital,
        data.education,
        data.default,
        data.balance,
        data.housing,
        data.loan
    ]

    df = pd.DataFrame([test_input], columns=DF_COLUMNS)
    X = prepare_sample(df)

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    pred_proba = proba[pred]

    return {
        "prediction": int(pred),
        "class_probabilities": proba.tolist(),
        "predicted_class_probability": float(pred_proba)
    }


def enrich_users_with_predictions(users):
    rows = [
        [
            u.age,
            u.job,
            u.marital,
            u.education,
            u.default,
            u.balance,
            u.housing,
            u.loan
        ]
        for u in users
    ]

    # Create dataframe & preprocess
    df = pd.DataFrame(rows, columns=DF_COLUMNS)
    X = prepare_sample(df)

    # Predict
    preds = model.predict(X)
    probas = model.predict_proba(X)

    # Attach predictions to user objects
    for user, pred, proba_vector in zip(users, preds, probas):
        pred_proba = proba_vector[pred]

        user.prediction = int(pred)
        user.probabilities = proba_vector.tolist()
        user.investmentPropensity = round(float(proba_vector[1]) * 100, 2)
        user.pred_proba = float(pred_proba)

    return users


@app.get("/api/fetch-user/{userId}")
async def fetch_user_by_id(userId: str):
    users = [u for u in users_db.values() if u.id == userId]
    if not users:
        return None
    enriched = enrich_users_with_predictions(users)
    return enriched[0]


@app.get("/api/fetch-users")
async def fetch_users():
    users = list(users_db.values())
    return enrich_users_with_predictions(users)


# Start server with following command:
# uvicorn main:app --reload
