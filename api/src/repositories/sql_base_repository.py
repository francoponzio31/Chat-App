from abc import ABC, abstractmethod
from repositories.sql_connection import get_db_session
from utilities.logger import logger
from utilities.customExceptions import EntityNotFoundError


class SQLBaseRepository(ABC):

    db_session = get_db_session()

    @property
    @abstractmethod
    def Model(self):
        raise NotImplementedError("Implement this method on all subclasses.")


    def get_all(self):
        return self.Model.query.all()


    def get_by_id(self, id:int):
        obj = self.Model.query.get(id)
        if not obj:
            raise EntityNotFoundError
        return obj


    def create_one(self, new_obj_data:dict):
        try:
            new_obj = self.Model(**new_obj_data)
            self.db_session.add(new_obj)
            self.db_session.commit()
            return new_obj
        except Exception as ex:
            logger.exception(str(ex))
            self.db_session.rollback()
            raise


    def update_one(self, id:int, updated_obj_data:dict):
        try:
            obj = self.get_by_id(id)
            for key, value in updated_obj_data.items():
                setattr(obj, key, value) 
            self.db_session.commit()
            return obj
        except Exception as ex:
            logger.exception(str(ex))
            self.db_session.rollback()
            raise


    def delete_one(self, id:int):
        try:
            obj = self.get_by_id(id)
            self.db_session.delete(obj)
            self.db_session.commit()
        except Exception as ex:
            logger.exception(str(ex))
            self.db_session.rollback()
            raise
