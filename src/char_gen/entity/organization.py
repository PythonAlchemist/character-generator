from typing import Union
from char_gen.base import Kanka


class Organization:
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.description: Union[str, None] = None

        if id:
            self.__existingEntity(id)
        else:
            self.__newEntity(props)

    def __newEntity(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def __existingEntityr(self, id: int) -> None:
        self.id = id
        resp = self.getCharacter(id)
        for k, v in resp.items():
            setattr(self, k, v)

    def __updateEntity(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def getOrganization(self, id: int):
        resp = Kanka.get(f"characters/{id}")
        return resp

    def getOrgList(self):
        resp = Kanka.get("organisations")
        return resp


if __name__ == "__main__":
    org = Organization()
    org.getOrgList()
