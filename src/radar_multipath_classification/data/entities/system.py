from datetime import datetime

import numpy as np
from attr import define, field
from hydra import compose
from pyquaternion import Quaternion
from shapely.geometry import MultiPoint, MultiPolygon

from radar_multipath_classification.data.entities.abstracts.entity import AbstractEntity
from radar_multipath_classification.data.entities.cpos import CartesianPosition


@define(frozen=True)
class System(AbstractEntity):
    time: datetime
    channel: str
    s2g: np.ndarray
    g2s: np.ndarray
    pos: CartesianPosition = field(init=False)
    orientation: Quaternion = field(init=False)
    coverage: MultiPolygon = field(init=False)

    def __attrs_post_init__(self):
        self._frozen_set(pos=CartesianPosition(*np.dot(self.s2g, [0, 0, 0, 1])[:3]))
        self._frozen_set(orientation=Quaternion(matrix=self.s2g))

        if self.channel == "RADAR":
            radar_cfg = compose(config_name="default").radar
            self._frozen_set(coverage=self._init_coverage(radar_cfg))

    def _init_coverage(self, radar_cfg):
        near_sector_poly = self._sector_polygon(radar_cfg.near_sector.range, np.deg2rad(radar_cfg.near_sector.azi))
        far_sector_poly = self._sector_polygon(radar_cfg.far_sector.range, np.deg2rad(radar_cfg.far_sector.azi))

        return MultiPolygon([near_sector_poly, far_sector_poly])

    def _sector_polygon(self, max_range, max_azimuth):
        sector_points = [
            [max_range * np.cos(theta), max_range * np.sin(theta), 0, 1] for theta in [-max_azimuth, 0, max_azimuth]
        ]
        sector_points = np.concatenate([[[0, 0, 0, 1]], sector_points])
        global_sector_points = np.dot(self.s2g, sector_points.T)

        return MultiPoint(global_sector_points[:2, :].T).convex_hull
