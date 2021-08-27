""" Geocoding

Geocoding is the process of transforming a description of a location—such 
as a pair of coordinates, an address, or a name of a place—to a location
on the earth's surface.

Address --> Coordinate(lat, lon)
"""

import requests
from typing import Union, Dict

from config import YANDEX_KEY
from constants import GEOCODE_URL


def get_coordinate(address: str) -> Union[Dict[float, float], None]:
    """ Returns the coordinate of a given address using Yandex Geocoding API.
        Returns None if the coordinate can not be grabed. 

        Parameters
        ----------
        address : The address whose coordinates you want to calculate. 
    """
    response = requests.get(GEOCODE_URL.format(YANDEX_KEY, address))
    data = response.json()

    if response.status_code == 200:
        # API returns a list of geoobjects. For example for 'ankara' there are
        # a few places and coordinates in different countries.
        geo_objects = data['response']['GeoObjectCollection']['featureMember']

        if len(geo_objects) == 0:
            return None

        # The first geoobjects's coordinate is probably what we want.
        data = geo_objects[0]['GeoObject']['Point']['pos']
        
        # data = '33.3333 44.4444'. So we need to split
        coordinate = data.split(' ')

        return {
            'lat': float(coordinate[1]),
            'lon': float(coordinate[0])
        }

    return None
