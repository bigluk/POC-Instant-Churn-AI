from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    prediction: Optional[int] = None
    investmentPropensity: Optional[float] = None
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
