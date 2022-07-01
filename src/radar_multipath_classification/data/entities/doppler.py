import numpy as np
from attr import define, field


@define(frozen=True)
class Doppler:
    x: float
    y: float
    is_positive: bool
    value: float = field(init=False)

    def __attrs_post_init__(self):
        self.value = ((2 * self.is_positive) - 1) * np.linalg.norm([self.x, self.y])
