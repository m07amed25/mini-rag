from fastapi import FastAPI, APIRouter
import os

baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["Base"]
)

@baseRouter.get("/")
async def welcome_message():
    appName = os.getenv("APP_NAME")
    appVersion = os.getenv("APP_VERSION")
    return {
        "message": f"Welcome to {appName} application!",
        "version": appVersion
        }
