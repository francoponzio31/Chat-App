from repositories.users.users_repository_interface import UsersRepositoryInterface
from repositories.json_base_repository import JSONBaseRepository
from models.user_models import UserJSONModel
from utilities.custom_exceptions import EntityNotFoundError


class JSONUserRepository(JSONBaseRepository[UserJSONModel], UsersRepositoryInterface):

    def __init__(self):
        super().__init__(filename="users.data.json")


    @property
    def Model(self) -> UserJSONModel:
        return UserJSONModel


    def get_by_email(self, user_email:str, raise_if_not_found:bool=True) -> UserJSONModel:
        users = self.get_all()
        searched_user = None
        for user in users:
            if user.email == user_email:
                searched_user = user
                break
        if not searched_user and raise_if_not_found:
            raise EntityNotFoundError
        return searched_user
