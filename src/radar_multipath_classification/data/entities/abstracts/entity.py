from abc import ABCMeta
from typing import Dict
from uuid import uuid4

from attr import define, field


@define
class AbstractEntity(metaclass=ABCMeta):
    __dict__: Dict = field(init=False, default={})
    uid: str = field(default=uuid4().hex, init=False)

    def _frozen_set(self, **kwargs):
        for name, value in kwargs.items():
            object.__setattr__(self, name, value)
