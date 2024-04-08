from schemas.user_schema import user_schema, users_schema
from repositories import users_repository
from utilities.customExceptions import EmailAlreadyRegistered


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


    def delete_user(self, user_id:int) -> None:
        users_repository.delete_one(user_id)


users_service = UsersService()
