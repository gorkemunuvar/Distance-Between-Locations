
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from constants import MKAD_KM


def in_polygon(lat: float, lon: float) -> bool:
    boundaries = [(x[2], x[1]) for x in MKAD_KM]

    point = Point(lat, lon)
    polygon = Polygon(boundaries)

    return polygon.contains(point)
