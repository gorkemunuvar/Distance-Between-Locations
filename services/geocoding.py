import requests
from typing import Union, Dict
from config import YANDEX_KEY
from constants import GEOCODE_URL


def get_position(address: str) -> Union[Dict[float, float], None]:
    response = requests.get(GEOCODE_URL.format(YANDEX_KEY, address))
    data = response.json()

    print(response.status_code)
    print(data)

    if response.status_code == 200:

        data = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        position = data.split(' ')

        return {
            'lat': float(position[1]),
            'lon': float(position[0])
        }

    return None
