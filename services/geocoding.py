import requests
from typing import Union, Dict
from config import YANDEX_KEY
from constants import GEOCODE_URL


def get_coordinate(address: str) -> Union[Dict[float, float], None]:
    response = requests.get(GEOCODE_URL.format(YANDEX_KEY, address))
    data = response.json()

    if response.status_code == 200:
        geo_objects = data['response']['GeoObjectCollection']['featureMember']

        if len(geo_objects) == 0:
            return None

        data = geo_objects[0]['GeoObject']['Point']['pos']
        coordinate = data.split(' ')

        return {
            'lat': float(coordinate[1]),
            'lon': float(coordinate[0])
        }

    return None
