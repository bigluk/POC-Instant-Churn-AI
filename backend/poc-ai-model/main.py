import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from common_utils import prepare_sample

app = FastAPI()

DF_COLUMNS = ["age", "job", "marital", "education", "default", "balance", "housing", "loan"]

# Load model
model = joblib.load("xgboost/xg-boost-model.pkl")


class Input(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str


@app.post("/predict")
def predict(data: Input):
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

# Start server with following command:
# uvicorn main:app --reload
