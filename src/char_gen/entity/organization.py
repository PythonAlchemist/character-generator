from typing import Union, List, Dict, Any
from char_gen.interface.base import Kanka
from char_gen.entity.core import Entity
from char_gen.entity.character import Character
import pandas as pd


class Organization(Entity):
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.description: Union[str, None] = None
        self.members: List[Dict[str, Any]] = []

        if id:
            self._existingEntity(id)
        else:
            self._newEntity(props)

    @staticmethod
    def getEntity(id: int):
        resp = Kanka.get(f"organisations/{id}")
        return resp

    @staticmethod
    def getEntityList():
        resp = Kanka.get("organisations")
        return resp

    @staticmethod
    def getAllMembers(id: int) -> List[Character]:
        resp = Organization.getEntity(id)
        members = [Character(id=member["character_id"]) for member in resp["members"]]

        return members

    def promptPackage(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "id": self.id,
        }


if __name__ == "__main__":
    org = Organization()
    org.getAllMembers(237897)
