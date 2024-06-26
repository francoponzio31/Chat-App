from abc import ABC, abstractmethod
from utilities.custom_exceptions import EntityNotFoundError
from utilities.utils import json_decoder, json_encoder
from config.app_config import config
import json
import os
from typing import Generic, TypeVar


T = TypeVar("T")

class JSONBaseRepository(Generic[T], ABC):

    """
    This class provide function with the basic CRUD operations for a JSON file persistance repository  
    """

    data_persistence_base_path = config.DATA_PERSISTENCE_PATH

    def __init__(self, filename):
        self.data_persistence_path = f"{self.data_persistence_base_path}/{filename}"
        os.makedirs(os.path.dirname(self.data_persistence_path), exist_ok=True)


    @property
    @abstractmethod
    def Model(self) -> T:
        raise NotImplementedError("Implement this method on all subclasses.")    


    def _load_data(self) -> list:
        try:
            with open(self.data_persistence_path, "r") as file:
                return json.load(file, object_hook=json_decoder)
        except FileNotFoundError:
            return []


    def _save_data(self, data) -> None:
        with open(self.data_persistence_path, "w") as file:
            json.dump(data, file, indent=4, default=json_encoder)


    def get_all(self) -> list[T]:
        objs = self._load_data()
        return [self.Model.from_dict(obj) for obj in objs]


    def get_by_id(self, id:int) -> T:
        objs = self.get_all()
        searched_obj = None
        for obj in objs:
            if obj.id == id:
                searched_obj = obj
                break
        if not searched_obj:
            raise EntityNotFoundError
        return searched_obj


    def create_one(self, new_obj_data:dict) -> T:
        objs = self.get_all()
        new_obj_data["id"] = 0 if not objs else objs[-1].id + 1
        new_obj = self.Model(**new_obj_data)
        objs.append(new_obj)
        self._save_data([obj.to_dict() for obj in objs])
        return new_obj


    def update_one(self, id:int, updated_obj_data:dict) -> T:
        objs = self.get_all()
        obj = self.get_by_id(id)
        for key, value in updated_obj_data.items():
            setattr(obj, key, value) 
        for index, u in enumerate(objs):
            if u.id == id:
                objs[index] = obj
                break
        self._save_data([obj.to_dict() for obj in objs])
        return obj


    def delete_one(self, id:int) -> None:
        objs = self.get_all()
        for index, obj in enumerate(objs):
            if obj.id == id:
                objs.pop(index)
                break
        self._save_data([obj.to_dict() for obj in objs])
        return obj
