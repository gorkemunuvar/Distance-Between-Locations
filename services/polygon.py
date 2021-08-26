
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from constants import MKAD_KM


def inside_polygon(lat: float, lon: float) -> bool:
    # To understnad if the specified address is located inside the MKAD
    # I used a simple mathematical trick. It check if the given point
    # is inside the given MKAD polygon using shapely module.  
    
    """Returns true if the given coordinate is inside the MKAD.

    Parameters
    ----------
    lat : Latitude value you want to check if inside MKAD polygon.
    lon : Longitude value you want to check if inside MKAD polygon.

    """

    statement1 = lat < -90 or lat > 90
    statement2 = lon < -180 or lon > 180

    # Corner case check
    if statement1 or statement2:
        return None

    # Eliminating index values from the MKAD list
    boundaries = [(x[2], x[1]) for x in MKAD_KM]

    point = Point(lat, lon)
    polygon = Polygon(boundaries)

    return polygon.contains(point)

