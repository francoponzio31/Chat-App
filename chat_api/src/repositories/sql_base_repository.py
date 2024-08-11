from abc import ABC, abstractmethod
from repositories.sql_connection import with_db_session, scoped_session
from utilities.custom_exceptions import EntityNotFoundError
from typing import Generic, TypeVar


T = TypeVar("T")

class SQLBaseRepository(Generic[T], ABC):

    """
    This class provide function with the basic CRUD operations for a SQL persistance repository.
    """

    @property
    @abstractmethod
    def Model(self) -> T:
        raise NotImplementedError("Implement this method on all subclasses.")


    @with_db_session
    def get_all(self, db_session:scoped_session=None) -> list[T]:
        return db_session.query(self.Model).all()


    @with_db_session
    def get_by_id(self, id:int, db_session:scoped_session=None) -> T:
        obj = db_session.query(self.Model).get(id)
        if not obj:
            raise EntityNotFoundError
        return obj


    @with_db_session
    def create_one(self, new_obj_data:dict, db_session:scoped_session=None) -> T:
        try:
            new_obj = self.Model(**new_obj_data)
            db_session.add(new_obj)
            db_session.commit()
            return new_obj
        except Exception:
            db_session.rollback()
            raise


    @with_db_session
    def update_one(self, id:int, updated_obj_data:dict, db_session:scoped_session=None) -> T:
        try:
            obj = db_session.query(self.Model).get(id)
            if not obj:
                raise EntityNotFoundError
            for key, value in updated_obj_data.items():
                setattr(obj, key, value) 
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            raise

    
    @with_db_session
    def delete_one(self, id:int, db_session:scoped_session=None) -> None:
        try:
            obj = db_session.query(self.Model).get(id)
            if not obj:
                raise EntityNotFoundError
            db_session.delete(obj)
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise
