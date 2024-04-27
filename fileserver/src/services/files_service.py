from repositories.fs_files_repository import FSFilesRepository
from repositories.s3_files_repository import S3FilesRepository
from fastapi import UploadFile
from config.app_config import config
from utilities.custom_exceptions import FileSizeExceededException, FileTypeNotAccepted
import mimetypes
from typing import Literal


class FileService:

    def __init__(self) -> None:
        self.repository = S3FilesRepository() if config.persistance_type == "S3" else FSFilesRepository()


    async def get_file_by_id(self, file_id:str, format:Literal["bytes", "b64"]) -> tuple[bytes | str, str]:
        file_content, filename, mime_type = await self.repository.get_file_by_id(file_id, format)
        return file_content, filename, mime_type


    async def upload_file(self, file:UploadFile) -> str:
        file_content = await file.read()

        extension = mimetypes.guess_extension(file.content_type)
        if extension not in config.allowed_files:
            raise FileTypeNotAccepted

        if len(file_content) > config.max_file_size:
            raise FileSizeExceededException

        file_id = await self.repository.upload_file(file_content)
        return file_id


    async def delete_file_by_id(self, file_id:str) -> None:
        await self.repository.delete_file_by_id(file_id)


file_service = FileService()
