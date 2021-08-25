from flask import Blueprint, request
from services.geocoding import get_position
from services.point_polygon import in_polygon
from services.distance import calculate_distance, calculate_distance_gh


distance_api = Blueprint('distance', __name__)


@distance_api.route('/', methods=['GET'])
def get_distance():
    address = request.args.get('address', None)
    print(f'Address: {address}')

    if address is None:
        return {'message': '<address> parameter is missing.'}

    position = get_position(address)
    print(position)

    in_polygon_result = in_polygon(position['lat'], position['lon'])

    print(f'in_polygon_result: {in_polygon_result}')

    if in_polygon_result:
        return {'message': 'No need to calculate'}, 200

    else:
        # Points were gotten from the link below
        # https://www.coordinatesfinder.com/coordinates/810957-66-km-mkad-moscow-russia
        source_lon = 37.3903193
        source_lat = 55.8142861
        target_lon = position['lon']
        target_lat = position['lat']

        distance = calculate_distance(source_lon, source_lat,
                                      target_lon, target_lat)

        return {'distance': distance}, 200
