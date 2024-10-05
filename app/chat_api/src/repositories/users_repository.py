from repositories.base_repository import SQLBaseRepository
from models.user_models import UserModel
from repositories.sql_connection import with_db_session, scoped_session
from utilities.custom_exceptions import EntityNotFoundError


class UserRepository(SQLBaseRepository[UserModel]):

    @property
    def Model(self) -> UserModel:
        return UserModel


    @with_db_session
    def get_by_email(self, user_email:str, raise_if_not_found:bool=True, db_session:scoped_session=None) -> UserModel:
        user = db_session.query(self.Model).filter_by(
            email = user_email
        ).one_or_none()
        if not user and raise_if_not_found:
            raise EntityNotFoundError(f"{str(self.Model())} with email {user_email} does not exists")
        return user


users_repository = UserRepository()