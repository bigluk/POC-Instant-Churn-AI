from typing import Optional, List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    age: int
    job: str
    marital: str
    education: str
    default_status: str
    balance: float
    housing: str
    loan: str
    prediction: Optional[int] = None
    investment_propensity: Optional[float]
    probabilities: Optional[list] = None
    pred_proba: Optional[float] = None


class ModelInput(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str


class ChartData(BaseModel):
    date: str
    ip: float


class PredictionOutput(BaseModel):
    prediction: int
    class_probabilities: List[float]
    predicted_class_probability: float
