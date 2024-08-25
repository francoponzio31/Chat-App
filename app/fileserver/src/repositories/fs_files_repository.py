from repositories.files_repository_interface import FilesRepositoryInterface
from uuid import uuid4
import aiofiles
import aiofiles.os as aio_os
import os


class FSFilesRepository(FilesRepositoryInterface):
    
    def __init__(self) -> None:
        self.files_folder = "./files"
        os.makedirs(os.path.dirname(self.files_folder), exist_ok=True)  # Creates the files folder if not exists


    async def get_file_by_id(self, file_id:str) -> bytes:
        file_location = f"{self.files_folder}/{file_id}"
        async with aiofiles.open(file_location, "rb") as file:
            file_content = await file.read()
        return file_content


    async def upload_file(self, file_content:bytes) -> str:
        file_id = str(uuid4())
        file_location = f"{self.files_folder}/{file_id}"
        async with aiofiles.open(file_location, "wb+") as file_object:
            await file_object.write(file_content)
        return file_id


    async def delete_file_by_id(self, file_id:str) -> None:
        file_location = f"{self.files_folder}/{file_id}"
        await aio_os.remove(file_location)
