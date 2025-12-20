from typing import Optional, List

from pydantic import BaseModel, ConfigDict


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
    inclined_to_invest: Optional[int] = None
    investment_propensity: Optional[float]


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


class AskRequest(BaseModel):
    projectId: int
    question: str
    threadId: Optional[str] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    type: Optional[str] = None
    explanation: Optional[str] = None
    threadId: Optional[str] = None
    sql: Optional[str] = None
    summary: Optional[str] = None
