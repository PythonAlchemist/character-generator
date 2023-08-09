from typing import Union
from char_gen.base import Kanka
from char_gen.entity.core import Entity
from char_gen.utils import extract_human_readable_text
import pandas as pd


class Character(Entity):
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.age: Union[int, None] = None
        self.description: Union[str, None] = None
        self.title: Union[str, None] = None
        self.type: Union[str, None] = None
        self.sex: Union[str, None] = None
        self.race: Union[str, None] = None
        self.family: Union[str, None] = None
        self.location: Union[str, None] = None
        self.organizations: Union[list, None] = None
        self.tags: Union[list, None] = None

        if id:
            self._existingEntity(id)
        else:
            self._newEntity(props)

    def __repr__(self) -> str:
        return f"Character: {self.name} \n Description: {self.description}"

    def toDF(self) -> pd.DataFrame:
        df = pd.DataFrame([self.__dict__])
        return df

    @staticmethod
    def getEntity(id: int):
        resp = Kanka.get(f"characters/{id}")
        return resp

    @staticmethod
    def getEntityList():
        resp = Kanka.get("characters")
        return resp

    def promptPackage(self):
        return {
            "name": self.name,
            "description": self.description,
            "title": self.title,
            "age": self.age,
            "sex": self.sex,
            "is_dead": self.is_dead,
            "organizations": self.organizations,
        }


if __name__ == "__main__":
    char1 = Character(id=1235133)
    a = 5
