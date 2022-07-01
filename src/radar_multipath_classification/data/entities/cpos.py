from typing import List

import numpy as np
from attr import define


@define(frozen=True)
class CartesianPosition:
    x: float
    y: float
    z: float

    @property
    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list)

    @property
    def to_4d_numpy(self) -> np.ndarray:
        return np.array([*self.to_list, 1])

    @property
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
