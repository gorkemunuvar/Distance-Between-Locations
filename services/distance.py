import requests
from typing import Union

from config import GRAPHHOPPER_KEY
from constants import ROUTING_URL_OSRM, ROUTING_URL_GHOPPER


def calculate_distance(source_lon: float, source_lat: float,
                       target_lon: float, target_lat: float) -> Union[float, None]:

    url = ROUTING_URL_OSRM.format(source_lon, source_lat,
                                  target_lon, target_lat)

    response = requests.get(url=url)
    data = response.json()

    if response.status_code == 200 and data.__contains__('code'):
        return data['routes'][0]['distance']

    return None


def calculate_distance_gh(source_lon: float, source_lat: float,
                          target_lon: float, target_lat: float) -> Union[float, None]:

    url = ROUTING_URL_GHOPPER.format(source_lat, source_lon,
                                     target_lat, target_lon, GRAPHHOPPER_KEY)
    response = requests.get(url=url)
    data = response.json()

    if response.status_code == 200:
        distance = data['paths'][0]['distance']
        return distance

    return None
