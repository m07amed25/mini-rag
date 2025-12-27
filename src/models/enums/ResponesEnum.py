from enum import Enum

class ResponsesEnum(str, Enum):
    FILE_VALIDATED = "File is valid."
    INVALID_FILE_TYPE = "Invalid file type."
    FILE_TOO_LARGE = "File size exceeds the maximum limit."
    FILE_UPLOADED_SUCCESSFULLY = "File is valid."
    FILE_UPLOAD_FAILED = "File upload failed."
