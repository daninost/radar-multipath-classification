from functools import cached_property, partial
from itertools import starmap
from typing import List

import numpy as np
from attr import define, field
from cytoolz import compose

from radar_multipath_classification.data.entities.abstracts.entity import AbstractEntity
from radar_multipath_classification.data.entities.cpos import CartesianPosition
from radar_multipath_classification.data.entities.ppos import PolarPosition
from radar_multipath_classification.data.entities.system import System


@define(frozen=True)
class AbstractSystemEntity(AbstractEntity):
    system: System
    pc: List[CartesianPosition] = field(converter=compose(list, partial(starmap, CartesianPosition)))
    polar_pc: List[PolarPosition] = field(init=False)

    def __attrs_post_init__(self):
        polar_pc = list(starmap(PolarPosition, self.polar_pc_list))
        self._frozen_set(polar_pc=polar_pc)

    @cached_property
    def length(self):
        return len(self.pc)

    @cached_property
    def pc_list(self):
        return [p.to_list for p in self.pc]

    @cached_property
    def pc_numpy(self):
        return np.array(self.pc_list)

    @cached_property
    def polar_pc_numpy(self):
        pc_numpy = self.pc_numpy.T
        rang = np.linalg.norm(pc_numpy[:2], 2, axis=0)
        azi = np.arctan2(pc_numpy[1], pc_numpy[0])
        return np.stack([rang, azi]).T

    @cached_property
    def polar_pc_list(self):
        return list(self.polar_pc_numpy)


def length_validator(inst, attr, value):
    if inst.length != len(value):
        raise ValueError(
            "{name} must have the same length as the given point cloud.\n"
            "Got {length} but expected {expected_length}".format(
                name=attr.name, length=len(value), expected_length=inst.length
            )
        )
