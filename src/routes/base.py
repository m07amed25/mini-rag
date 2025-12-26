from fastapi import FastAPI, APIRouter
import os

baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["Base"]
)

@baseRouter.get("/")
async def welcome_message():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message": f"Welcome to {app_name} application!",
        "version": app_version
        }
