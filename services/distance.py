

import requests
from typing import Union

from constants import ROUTING_URL_OSRM, MKAD_LONGITUDE, MKAD_LATITUDE


def calculate_distance(target_lon: float, target_lat: float) -> Union[float, None]:
    # To calculate the distance between two coordinate a Routing Machine
    # must be used. Instead of using Yandex Routing Machine, Open Street
    # Routing Machine was prefered here because it is open source and free.
    """Calculates the distance between MKAD and the given coordinate of an address.
       Returns None if the distance value does not exist in response.

       Parameters
       ----------
       target_lon : Target longitude you want to calculate the distance to from MKAD.
       target_lat : Target latitude you want to calculate the distance to from MKAD.
    """

    url = ROUTING_URL_OSRM.format(target_lon, target_lat)

    response = requests.get(url=url)
    data = response.json()

    if response.status_code == 200 and data.__contains__('code'):
        return data['routes'][0]['distance']

    return None
