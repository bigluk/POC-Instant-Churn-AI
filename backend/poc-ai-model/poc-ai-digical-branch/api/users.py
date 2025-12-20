from typing import List, Dict

import httpx
from fastapi import APIRouter, HTTPException

from core.models import PredictionOutput, ModelInput, ChartData, User, TaskResponse, AskRequest
from services.chart_service import ChartService
from services.prediction_service import PredictionService
from services.user_service import UserService

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/update-prediction/{user_id}", response_model=PredictionOutput)
async def update_prediction_for_user(user_id: str, data: ModelInput):
    predictionService = PredictionService()
    pred, probs, pred_prob = predictionService.predict_single(data.model_dump())

    userService = UserService()
    userService.update_user_propensity(user_id, probs[1], pred)

    return PredictionOutput(
        prediction=pred,
        class_probabilities=probs,
        predicted_class_probability=pred_prob
    )


@router.get("/update-predictions", response_model=List[Dict])
async def update_predictions():
    userService = UserService()
    users = userService.get_all_users()

    predictionService = PredictionService()
    predictions_data = predictionService.predict_batch(users)

    for user, (pred, probabilities, pred_proba) in zip(users, predictions_data):
        investment_propensity = round(float(probabilities[1]) * 100, 2)
        userService.update_user_propensity(user['id'], investment_propensity, pred)
        user['prediction'] = pred
        user['investment_propensity'] = investment_propensity
        user['pred_proba'] = pred_proba
        user['probabilities'] = probabilities

    return users


@router.get("/fetch-users", response_model=List[User])
async def get_all_users():
    service = UserService()
    return service.get_all_users()


@router.get("/fetch-user/{user_id}", response_model=User)
async def get_user(user_id: str):
    service = UserService()
    user = service.get_user(user_id)
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


@router.post("/ask-to-ai", response_model=TaskResponse)
async def ask_to_ai(request: AskRequest):
    payload = {
        "projectId": request.projectId,
        "question": request.question
    }

    if request.threadId is not None:
        payload["threadId"] = request.threadId

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post("http://localhost:3000/api/v1/ask", json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {e}")

    return data

