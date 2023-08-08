from typing import Union
from src.base import Kanka


class Character:
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
            self.__existingCharacter(id)
        else:
            self.__newCharacter(props)

    def __newCharacter(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def __existingCharacter(self, id: int) -> None:
        self.id = id
        resp = self.getCharacter(id)
        for k, v in resp.items():
            setattr(self, k, v)

    def __updateCharacter(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def getCharacter(self, id: int):
        resp = Kanka.get(f"characters/{id}")
        return resp

    def getCharacterList(self):
        resp = Kanka.get("characters")
        return resp


if __name__ == "__main__":
    char1 = Character(id=1235133)
    char2 = Character(
        props={
            "name": "Test",
            "age": 100,
            "description": "This is a test",
        }
    )
    s = 6
