from fastapi import APIRouter, Depends
import os
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"]
)

@base_router.get("/")
async def welcome_message(settings: Settings = Depends(get_settings)):
    # settings = get_settings()

    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION

    return {
        "message": f"Welcome to {app_name} application!",
        "version": app_version
        }
