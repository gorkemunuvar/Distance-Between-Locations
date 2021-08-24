import requests
from urllib import request
from config import YANDEX_KEY, GRAPHHOPPER_KEY
from constants import MKAD_KM
from haversine import haversine, Unit
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

GEOCODE_URL = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&format=json&geocode={}&lang=en-US'
ROUTING_URL_OSRM = 'http://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=false'
ROUTING_URL_GHOPPER = 'https://graphhopper.com/api/1/route?point={},{}&point={},{}&vehicle=car&locale=de&calc_points=false&key={}'


if __name__ == '__main__':
    # Points were gotten from the link below
    # https://www.coordinatesfinder.com/coordinates/810957-66-km-mkad-moscow-russia
    source_lon = 37.3903193
    source_lat = 55.8142861

    target_address = input('Address: ')
    routing_engine = input('Routing Engine: ')

    # Get points from the address with Yandex Map API
    response = requests.get(GEOCODE_URL.format(YANDEX_KEY, target_address))
    data = response.json()

    position = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(
        ' ')

    target_lon = float(position[0])
    target_lat = float(position[1])

    boundaries = [(x[2], x[1]) for x in MKAD_KM]

    point = Point(target_lat, target_lon)
    polygon = Polygon(boundaries)

    in_polygon = polygon.contains(point)

    # If the specified address is located inside the MKAD
    if in_polygon:
        # Distance does not to be calculated
        print('Distance does not to be calculated')
        # return

    # Calculate difference between points
    else:
        if routing_engine == 'osrm':
            routing_url = ROUTING_URL_OSRM.format(
                source_lon, source_lat, target_lon, target_lat)
            response = requests.get(url=routing_url)

            data = response.json()
            if response.status_code == 200 and data.__contains__('code'):
                print(data['routes'][0]['distance'])
                
        if routing_engine == 'gh':
            routing_url = ROUTING_URL_GHOPPER.format(
                source_lat, source_lon, target_lat, target_lon, GRAPHHOPPER_KEY)
            response = requests.get(url=routing_url)

            data = response.json()
            if response.status_code == 200:
                distance = data['paths'][0]['distance']
                print(distance)
