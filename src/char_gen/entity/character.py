from typing import Union
from char_gen.interface.base import Kanka
from char_gen.entity.core import Entity
from char_gen.utils import extract_human_readable_text
import pandas as pd
import json


class Character(Entity):
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.age: Union[str, None] = None
        self.description: Union[str, None] = None
        self.backstory: Union[str, None] = None
        self.title: Union[str, None] = None
        self.type: Union[str, None] = None
        self.sex: Union[str, None] = None
        self.race: Union[str, None] = None
        self.family: Union[str, None] = None
        self.location: Union[str, None] = None
        self.organizations: Union[list, None] = None
        self.tags: Union[list, None] = None
        self.is_dead: bool = False

        if id:
            self._existingEntity(id)
        else:
            self._newEntity(props)

    def __repr__(self) -> str:
        return f"Character: {self.name} \n Description: {self.description}"

    def toDF(self) -> pd.DataFrame:
        df = pd.DataFrame([self.__dict__])
        return df

    def upload(self):
        payload = self.promptPackage()

        # adjust payload keys
        payload["entry"] = self.description + "\n\n" + self.backstory
        del payload["description"]
        del payload["backstory"]

        resp = Kanka.post("characters", payload=payload)
        return resp

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
            "backstory": self.backstory,
            "title": self.title,
            "age": self.age,
            "sex": self.sex,
        }


if __name__ == "__main__":
    resp = {
        "name": "Elysia",
        "description": "Elysia is a graceful and ethereal figure, embodying the beauty and magic of the Moonshadow Grove. Standing at an average height, she carries herself with an air of quiet confidence. Her skin is fair and radiant, glowing softly in the moonlight. Cascading down her back is a mane of silver-white hair, adorned with delicate flowers and intertwined with subtle vines. Elysia's eyes are a mesmerizing shade of pale blue, shimmering with a deep wisdom and a hint of moonlit magic. Her voice is melodic and soothing, resonating with the calm energy of the grove. She possesses an aura of serenity, and animals are drawn to her calming presence.",
        "backstory": "Elysia was a wanderer before she discovered Moonshadow Grove. Drawn by the whispers of ancient spirits, she found solace and purpose in the grove's serene beauty. Under the guidance of Davnan, she honed her druidic abilities and developed a profound connection with the lunar cycle. Elysia quickly gained a reputation among the Moon Druids for her exceptional skill in harnessing the energy of the moon and communing with nature spirits. Her deep respect for the balance of nature and her unwavering dedication to preserving it have earned her the trust and admiration of her fellow druids.",
        "age": "126",
        "title": "Lunar Guardian",
        "race": "Elf",
        "sex": "Female",
    }

    char1 = Character(props=resp)
    char1
