from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from services.emails_service import emails_service as service
from schemas.inputs import EmailDataInput
from schemas.outputs import BaseResponse, ErrorResponse
from utilities.logger import logger


emails_router = APIRouter()

@emails_router.post("/send", response_model=BaseResponse, tags=["emails"])
async def send_email(email_data: EmailDataInput = Body(...)):
    try:
        await service.send_email(email_data)
        return JSONResponse(content=BaseResponse(success=True, message="Email sent successfully").model_dump())
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=ErrorResponse(success=False, message="Error sending email").model_dump(), status_code=500)