from typing import List

from fastapi import APIRouter, HTTPException

from core.models import PredictionOutput, ModelInput, ChartData, User
from services.chart_service import ChartService
from services.prediction_service import PredictionService
from services.user_service import UserService

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/predict", response_model=PredictionOutput)
async def predict(data: ModelInput):
    predictionService = PredictionService()
    user_id = data.user_id
    pred, probs, pred_prob = predictionService.predict_single(data.model_dump())

    userService = UserService()
    userService.update_user_propensity(user_id, probs[1])

    return PredictionOutput(
        prediction=pred,
        class_probabilities=probs,
        predicted_class_probability=pred_prob
    )


@router.get("/fetch-users", response_model=List[User])
async def get_all_users():
    service = UserService()
    return service.get_all_enriched_users()


@router.get("/fetch-user/{user_id}", response_model=User)
async def get_user(user_id: str):
    service = UserService()
    user = service.get_enriched_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/chart/{user_id}", response_model=List[ChartData])
async def get_user_chart(user_id: str):
    service = ChartService()
    chart_data = service.get_user_propensity_chart(user_id)

    if not chart_data:
        raise HTTPException(status_code=404, detail="No chart data found")

    return chart_data
