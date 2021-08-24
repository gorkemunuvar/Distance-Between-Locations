from operator import pos
import requests
from typing import Dict, Union
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from config import YANDEX_KEY, GRAPHHOPPER_KEY
from constants import GEOCODE_URL, ROUTING_URL_OSRM, ROUTING_URL_GHOPPER, MKAD_KM


class DistanceService:
    @classmethod
    def __get_position(cls, address: str) -> Union[Dict[float, float], None]:
        response = requests.get(GEOCODE_URL.format(YANDEX_KEY, address))
        data = response.json()

        if response.status_code == 200:
            data = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            position = data.split(' ')

            return {
                'lat': float(position[1]),
                'lon': float(position[0])
            }

        return None

    @classmethod
    def __in_polygon(cls, lat: float, lon: float) -> bool:
        boundaries = [(x[2], x[1]) for x in MKAD_KM]

        point = Point(lat, lon)
        polygon = Polygon(boundaries)

        return polygon.contains(point)

    @classmethod
    def __calc_dist_osrm(cls,
                         source_lon: float,
                         source_lat: float,
                         target_lon: float,
                         target_lat: float) -> Union[float, None]:

        url = ROUTING_URL_OSRM.format(
            source_lon, source_lat, target_lon, target_lat)

        response = requests.get(url=url)
        data = response.json()

        if response.status_code == 200 and data.__contains__('code'):
            return data['routes'][0]['distance']

        return None

    @classmethod
    def __calc_dist_gh(cls,
                       source_lon: float,
                       source_lat: float,
                       target_lon: float,
                       target_lat: float) -> Union[float, None]:

        url = ROUTING_URL_GHOPPER.format(
            source_lat, source_lon, target_lat, target_lon, GRAPHHOPPER_KEY
        )
        response = requests.get(url=url)
        data = response.json()

        if response.status_code == 200:
            distance = data['paths'][0]['distance']
            return distance

        return None

    @classmethod
    def calculate_distance(cls, address: str) -> Union[float, None]:
        position = cls.__get_position(address)
        in_polygon = cls.__in_polygon(position['lat'], position['lon'])

        if in_polygon:
            print('No need to calculate')
        else:
            # Points were gotten from the link below
            # https://www.coordinatesfinder.com/coordinates/810957-66-km-mkad-moscow-russia
            source_lon = 37.3903193
            source_lat = 55.8142861

            target_lon = position['lon']
            target_lat = position['lat']

            distance = cls.__calc_dist_osrm(
                source_lon,
                source_lat,
                target_lon,
                target_lat
            )

            return distance
        return None
