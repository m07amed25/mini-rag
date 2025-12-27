import os
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponsesEnum
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024

    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponsesEnum.INVALID_FILE_TYPE.value

        if file.size > self.settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponsesEnum.FILE_TOO_LARGE.value
        
        file.file.seek(0)

        return True, ResponsesEnum.FILE_VALIDATED.value

    def generate_unique_filename(self, original_filename: str, id: str) -> str:
        random_file_name = self.generate_random_string()
        project_folder = ProjectController().get_project_path(id)

        cleaned_filename = self.get_clean_filename(original_filename)
        
        new_file_path = os.path.join(
            project_folder, f"{random_file_name}_{cleaned_filename}"
            )
        
        while os.path.exists(new_file_path):
            random_file_name = self.generate_random_string()
            new_file_path = os.path.join(
                project_folder, f"{random_file_name}_{cleaned_filename}"
                )

        return new_file_path

    def get_clean_filename(self, filename: str) -> str:
        cleaned_filename = re.sub(r"[^/w.], ", "_", filename)
        cleaned_filename = re.sub(" ", "_", cleaned_filename)

        return cleaned_filename