from repositories import users_repository
from integrations.fileserver_client import fs_client


class UsersService:
        
    def get_users(self, limit:int|None=None, offset:int|None=None, username:str|None=None) -> list[dict]:
        return users_repository.get_all(offset=offset, limit=limit, username=username)
  

    def get_user_by_id(self, user_id:int) -> dict:
        return users_repository.get_by_id(user_id)


    def update_user(self, user_id:int, **kwargs) -> dict:
        return users_repository.update_one(user_id, **kwargs)


    def get_user_picture(self, user_id:int) -> str | None:
        user = users_repository.get_by_id(user_id)
        if not user.picture_id:
            return None
        file_content = fs_client.get_file_content(user.picture_id)
        return file_content


    def update_user_picture(self, user_id:int, content:bytes, filename:str) -> str:
        file_id = fs_client.upload_file(content, filename)
        user = users_repository.update_one(user_id, picture_id=file_id)
        return user.picture_id


    def delete_user(self, user_id:int) -> None:
        users_repository.delete_one(user_id)


users_service = UsersService()
