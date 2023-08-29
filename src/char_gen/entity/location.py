from typing import Union
from char_gen.interface.base import Kanka
from char_gen.entity.core import Entity


class Location(Entity):
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.description: Union[str, None] = None

        if id:
            self._existingEntity(id)
        else:
            self._newEntity(props)

    def __repr__(self) -> str:
        return f"Location: {self.name} \nDescription: {self.description}"

    @staticmethod
    def getEntity(id: int):
        resp = Kanka.get(f"locations/{id}")
        return resp

    @staticmethod
    def getEntityList():
        resp = Kanka.get("locations")
        return resp

    def promptPackage(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }


if __name__ == "__main__":
    loc = Location(1112563)
    print(loc)
