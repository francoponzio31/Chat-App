from repositories.fs_files_repository import FSFilesRepository
from repositories.s3_files_repository import S3FilesRepository
from config.app_config import config
from utilities.utils import validate_uuid_format
from utilities.custom_exceptions import InvalidFileID, MaxFileSizeExceeded, FileTypeNotAccepted
import mimetypes
import magic
import base64
from typing import Literal



class FileService:

    def __init__(self) -> None:
        self.repository = S3FilesRepository() if config.persistance_type == "S3" else FSFilesRepository()
        self.mime = magic.Magic(mime=True)


    async def get_file_by_id(self, file_id:str, format:Literal["bytes", "b64"]) -> tuple[bytes | str, str]:
        if not validate_uuid_format(file_id):
            raise InvalidFileID 

        file_content = await self.repository.get_file_by_id(file_id)
        mime_type = self.mime.from_buffer(file_content)
        file_extension = mimetypes.guess_extension(mime_type)
        filename = f"{file_id}{file_extension}"

        if format == "b64":
            file_content = base64.b64encode(file_content).decode("utf-8")
        
        return file_content, filename, mime_type


    async def upload_file(self, file_content:bytes) -> str:
        mime_type = self.mime.from_buffer(file_content)
        file_extension = mimetypes.guess_extension(mime_type)

        if file_extension not in config.allowed_files:
            raise FileTypeNotAccepted

        if len(file_content) > config.max_file_size:
            raise MaxFileSizeExceeded

        file_id = await self.repository.upload_file(file_content)
        return file_id


    async def delete_file_by_id(self, file_id:str) -> None:
        await self.repository.delete_file_by_id(file_id)


files_service = FileService()
