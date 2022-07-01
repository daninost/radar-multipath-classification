from typing import List

from attr import define, field

from radar_multipath_classification.data.entities.abstracts.sysentity import AbstractSystemEntity, length_validator


@define(frozen=True)
class Lidar(AbstractSystemEntity):
    intensities: List[float] = field(validator=length_validator)
