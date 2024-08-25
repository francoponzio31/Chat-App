from abc import ABC, abstractmethod
from typing import Literal, Awaitable


class FilesRepositoryInterface(ABC):

    @abstractmethod
    async def get_file_by_id(self, file_id:str, format:Literal["bytes", "b64"]) -> Awaitable[tuple[bytes | str, str]]:
        raise NotImplementedError("Implement this method on all subclasses.")

    @abstractmethod
    async def upload_file(self, file_content:bytes) -> Awaitable[str]:
        raise NotImplementedError("Implement this method on all subclasses.")

    @abstractmethod
    async def delete_file_by_id(self, file_id:str) -> Awaitable[None]:
        raise NotImplementedError("Implement this method on all subclasses.")
