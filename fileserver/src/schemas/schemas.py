from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    success: bool = Field(None, description="Response success")
    message: str = Field(None, description="Response message")

class ErrorResponse(BaseResponse):
    success: bool = False

class FileUploadResponse(BaseResponse):
    success: bool = True
    file_id: str = Field(None, description="The unique identifier for the file")

class FileResponse(BaseResponse):
    success: bool = True
    file: str = Field(None, description="Base64 encoded content of the file")
    filename: str = Field(None, description="Name of the file")
