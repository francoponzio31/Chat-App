from repositories.users.users_repository_interface import UsersRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.user_models import UserSQLModel
from repositories.sql_connection import with_db_session, scoped_session
from utilities.custom_exceptions import EntityNotFoundError


class SQLUserRepository(SQLBaseRepository[UserSQLModel], UsersRepositoryInterface):

    @property
    def Model(self) -> UserSQLModel:
        return UserSQLModel


    @with_db_session
    def get_by_email(self, user_email:str, raise_if_not_found:bool=True, db_session:scoped_session=None) -> UserSQLModel:
        user = db_session.query(self.Model).filter_by(
            email = user_email
        ).one_or_none()
        if not user and raise_if_not_found:
            raise EntityNotFoundError
        return user
    
    def get_filtered(self, limit=None|int, offset=None|int, db_session:scoped_session=None, **kwargs):
        query = db_session.query(self.Model)
        
        if kwargs:
            query = query.filter_by(**kwargs)

        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()

