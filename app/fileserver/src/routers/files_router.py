from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response, JSONResponse
from services.files_service import files_service as service
from utilities.custom_exceptions import InvalidFileID, MaxFileSizeExceeded, FileTypeNotAccepted
from schemas.schemas import FileUploadResponse, FileResponse, ErrorResponse, BaseResponse
from utilities.logger import logger


files_router = APIRouter()

@files_router.get("/{file_id}/content", response_model=FileResponse, tags=["files"])
async def get_file_by_id(file_id):
    try:
        file_content, filename, _ = await service.get_file_by_id(file_id, format="b64")
        return JSONResponse(content=FileResponse(message="File obtained successfully", content=file_content, filename=filename).model_dump())
    except InvalidFileID as ex:
        return JSONResponse(content=ErrorResponse(message=ex.message).model_dump(), status_code=400)
    except FileNotFoundError:
        return JSONResponse(content=ErrorResponse(message="File not found").model_dump(), status_code=404)
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=ErrorResponse(message="Error getting the file").model_dump(), status_code=500)


@files_router.get("/{file_id}/download", response_class=Response, tags=["files"])
async def download_file_by_id(file_id):
    try:
        file_content, filename, mime_type = await service.get_file_by_id(file_id, format="bytes")
        return Response(
            content=file_content,
            media_type=mime_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except InvalidFileID as ex:
        return JSONResponse(content=ErrorResponse(message=ex.message).model_dump(), status_code=400)
    except FileNotFoundError:
        return JSONResponse(content=ErrorResponse(message="File not found").model_dump(), status_code=404)
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=ErrorResponse(message="Error getting the file").model_dump(), status_code=500)


@files_router.post("", response_model=FileUploadResponse, tags=["files"])
async def upload_file(file:UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_id = await service.upload_file(file_content)
        return JSONResponse(content=FileUploadResponse(message="File uploaded successfully", file_id=file_id).model_dump())
    except FileTypeNotAccepted as ex:
        return JSONResponse(content=ErrorResponse(message=ex.message).model_dump(), status_code=400)
    except MaxFileSizeExceeded as ex:
        return JSONResponse(content=ErrorResponse(message=ex.message).model_dump(), status_code=400)
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=ErrorResponse(message="Error uploading file").model_dump(), status_code=500)
    finally:
        await file.close()


@files_router.delete("/{file_id}", response_model=BaseResponse, tags=["files"])
async def delete_file_by_id(file_id):
    try:
        await service.delete_file_by_id(file_id)
        return JSONResponse(content=BaseResponse(success=True, message="File deleted successfully").model_dump())
    except FileNotFoundError:
        return JSONResponse(content=ErrorResponse(message="File not found").model_dump(), status_code=404)
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=ErrorResponse(message="Error deleting file").model_dump(), status_code=500)
