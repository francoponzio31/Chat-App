from schemas.user_schema import user_schema, users_schema
from schemas.inputs_schemas import picture_schema
from repositories import users_repository
from integrations.fileserver_client import fs_client
from utilities.custom_exceptions import EmailAlreadyRegistered


class UsersService:
        
    def get_users(self) -> list[dict]:
        users = users_repository.get_all()
        return users_schema.dump(users)


    def get_user_by_id(self, user_id:int) -> dict:
        user = users_repository.get_by_id(user_id)
        return user_schema.dump(user)


    def create_user(self, new_user_data:dict) -> dict:
        new_user_data = user_schema.load(new_user_data)
        email_already_registered = users_repository.get_by_email(new_user_data["email"], raise_if_not_found=False)
        if email_already_registered:
            raise EmailAlreadyRegistered
        new_user = users_repository.create_one(new_user_data)
        return user_schema.dump(new_user)


    def update_user(self, user_id:int, updated_user_data:dict) -> dict:
        updated_user_data = user_schema.load(updated_user_data, partial=True)
        user = users_repository.update_one(user_id, updated_user_data)
        return user_schema.dump(user)


    def get_user_picture(self, user_id:int) -> str:
        user = users_repository.get_by_id(user_id)
        file_content = fs_client.get_file_content(user.picture_id)
        return file_content


    def update_user_picture(self, user_id:int, picture_data:dict) -> str:
        picture_data = picture_schema.load(picture_data)
        file_id = fs_client.upload_file(picture_data["content"], picture_data["filename"])
        user = users_repository.update_one(user_id, {"picture_id": file_id})
        return user.picture_id


    def delete_user(self, user_id:int) -> None:
        users_repository.delete_one(user_id)


users_service = UsersService()
