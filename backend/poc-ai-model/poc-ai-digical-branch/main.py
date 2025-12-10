from fastapi import FastAPI
from api import users

app = FastAPI(title="Investment Propensity API")

# routes register
app.include_router(users.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Start server with following command:
# uvicorn main:app --reload
