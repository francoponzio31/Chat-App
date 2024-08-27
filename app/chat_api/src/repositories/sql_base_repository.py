from abc import ABC, abstractmethod
from repositories.sql_connection import with_db_session, scoped_session
from utilities.custom_exceptions import EntityNotFoundError
from typing import Generic, TypeVar
import copy


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
    def get_all(self, limit:int|None, offset:int|None, db_session:scoped_session=None, **kwargs) -> tuple[list[T], int]:
        query = db_session.query(self.Model)

        for key, value in kwargs.items():
            if value is None:
                continue
            if isinstance(value, str):
                # # Apply LIKE filter for str fields
                query = query.filter(getattr(self.Model, key).like(f"%{value}%"))
            else:
                # Apply equality filter for other data types
                query = query.filter_by(**{key: value})

        total_records = query.count()

        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all(), total_records


    @with_db_session
    def get_by_id(self, id:int, db_session:scoped_session=None) -> T:
        obj = db_session.query(self.Model).get(id)
        if not obj:
            raise EntityNotFoundError
        return obj


    @with_db_session
    def create_one(self, db_session:scoped_session=None, **kwargs) -> T:
        try:
            new_obj = self.Model(**kwargs)
            db_session.add(new_obj)
            db_session.commit()
            return new_obj
        except Exception:
            db_session.rollback()
            raise


    @with_db_session
    def update_one(self, id:int, return_original:bool=False, db_session:scoped_session=None, **kwargs) -> T:
        try:
            obj = db_session.query(self.Model).get(id)
            if not obj:
                raise EntityNotFoundError
            
            original_obj = copy.deepcopy(obj)

            for key, value in kwargs.items():
                setattr(obj, key, value) 
            db_session.commit()

            return original_obj if return_original else obj
        
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
