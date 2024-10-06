from repositories.users_repository import users_repository
from models.user_models import UserModel
from integrations.fileserver_client import fs_client


class UsersService:
        
    def get_users(self, user_id:int, limit:int|None=None, offset:int|None=None, username:str|None=None, is_verified:bool=True, exclude_current_user:bool=False) -> tuple[list[UserModel], int]:
        return users_repository.get_all(
            offset=offset,
            limit=limit,
            username=username,
            is_verified=is_verified,
            exclude_ids=[user_id] if exclude_current_user else []
        )


    def get_user_by_id(self, user_id:int) -> UserModel:
        return users_repository.get_by_id(user_id)


    def update_user(self, user_id:int, **kwargs) -> UserModel:
        return users_repository.update_one(user_id, **kwargs)


    def get_user_picture(self, user_id:int) -> str | None:
        user = users_repository.get_by_id(user_id)
        if not user.picture_id:
            return None
        file_content = fs_client.get_file_content(user.picture_id)
        return file_content


    def update_user_picture(self, user_id:int, content:bytes, filename:str) -> str:
        new_picture_file_id = fs_client.upload_file(content, filename)
        user_before_update = users_repository.update_one(user_id, picture_id=new_picture_file_id, return_original=True)
        
        older_picture_file_id = user_before_update.picture_id
        if older_picture_file_id:
            fs_client.delete_file(older_picture_file_id)
        
        return user_before_update.picture_id


users_service = UsersService()
