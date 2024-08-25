from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    success: bool = Field(None, description="Response success")
    message: str = Field(None, description="Response message")

class ErrorResponse(BaseResponse):
    success: bool = False
