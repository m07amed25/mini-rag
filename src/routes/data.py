from fastapi import APIRouter, UploadFile, File, Depends, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import aiofiles
from models import ResponsesEnum
import logging

logger = logging.getLogger("uvicorn.error")    

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "Data"]
)

@data_router.post("/upload/{id}")
async def upload_data(
    id: str, 
    file: UploadFile = File(...), 
    settings: Settings = Depends(get_settings)
):
    Data = DataController()
    # Validate the file properties
    is_valid, message = Data.validate_uploaded_file(file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": message
            }
        )
    
    project_dir_path = ProjectController().get_project_path(id)

    file_path =  Data.generate_unique_filename(file.filename, id)
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Failed to upload file: {str(e)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": f"Failed to upload file: {str(e)}",
                "signal": ResponsesEnum.FILE_UPLOAD_FAILED
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "signal": ResponsesEnum.FILE_UPLOADED_SUCCESSFULLY,
            "detail": f"File '{file.filename}' uploaded successfully to project '{id}'."
        }
    )