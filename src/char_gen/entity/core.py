from abc import ABC, abstractmethod
from typing import Union
from char_gen.utils import extract_human_readable_text
import pandas as pd


class Entity(ABC):
    def __init__(self, id: Union[int, None] = None, props: dict = {}):
        self.id: Union[int, None] = None
        self.name: Union[str, None] = None
        self.description: Union[str, None] = None

    def _newEntity(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def _existingEntity(self, id: int) -> None:
        self.id = id
        resp = self.getEntity(id)
        for k, v in resp.items():
            setattr(self, k, v)

        # parse html
        self.description = extract_human_readable_text(self.entry_parsed)

    def _updateEntity(self, props: dict) -> None:
        for k, v in props.items():
            setattr(self, k, v)

    def toDF(self) -> pd.DataFrame:
        df = pd.DataFrame([self.__dict__])
        return df

    @abstractmethod
    def getEntity(id: int):
        raise NotImplementedError

    @abstractmethod
    def getEntityList():
        raise NotImplementedError
