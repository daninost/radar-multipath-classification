from attr import define


@define(frozen=True)
class PolarPosition:
    range: float
    azimuth: float
