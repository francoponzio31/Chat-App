from repositories.users.users_repository_interface import UsersRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.user_models import UserSQLModel
from utilities.customExceptions import EntityNotFoundError


class SQLUserRepository(SQLBaseRepository, UsersRepositoryInterface):

    @property
    def Model(self) -> UserSQLModel:
        return UserSQLModel


    def get_by_email(self, user_email:str, raise_if_not_found:bool=True) -> UserSQLModel:
        user = self.Model.query.filter_by(
            email = user_email
        ).one_or_none()
        if not user and raise_if_not_found:
            raise EntityNotFoundError
        return user
