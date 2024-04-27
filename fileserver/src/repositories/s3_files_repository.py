from repositories.files_repository_interface import FilesRepositoryInterface
from typing import Awaitable
from dotenv import load_dotenv
from aioboto3 import Session
from typing import Literal
from uuid import uuid4
import mimetypes
import base64
import os


load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


class S3FilesRepository(FilesRepositoryInterface):

    def __init__(self):
        self.bucket_name = AWS_S3_BUCKET


    async def get_s3_client(self):
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return session.client("s3")
    

    async def get_file_by_id(self, file_id: str, format: Literal["bytes", "b64"]) -> Awaitable[tuple[bytes | str, str, str]]:
        async with await self.get_s3_client() as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=file_id)
            file_content = await response["Body"].read()

        mime_type = self.mime.from_buffer(file_content)
        file_extension = mimetypes.guess_extension(mime_type)
        filename = f"{file_id}{file_extension}"

        if format == "b64":
            file_content = base64.b64encode(file_content).decode("utf-8")

        return file_content, filename, mime_type


    async def upload_file(self, file_content: bytes) -> Awaitable[str]:
        file_id = str(uuid4())
        async with await self.get_s3_client() as s3:
            await s3.put_object(Bucket=self.bucket_name, Key=file_id, Body=file_content)
        return file_id


    async def delete_file_by_id(self, file_id: str) -> Awaitable[None]:
        async with await self.get_s3_client() as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=file_id)
