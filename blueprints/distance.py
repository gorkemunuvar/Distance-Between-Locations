import logging
from flask import Blueprint, request

import returning_strings as r
from services.geocoding import get_coordinate
from services.polygon import inside_polygon
from services.distance import calculate_distance


distance_api = Blueprint('distance', __name__)


@distance_api.route('/', methods=['GET'])
def get_distance():
    # Get address from query string parameters.
    address = request.args.get('address', None)

    if address is None:
        return {'message': r.ADDRESS_MISSING}, 400

    # Get latitude and longitude using the given address.
    coordinate = get_coordinate(address.lower())

    if coordinate is None:
        logging.error(msg=r.ADDRESS_WARNING)
        return {'message': r.ADDRESS_WARNING}, 400

    # Check whether if the coordinate is inside MKAD.
    inside_polygon_result = inside_polygon(coordinate['lat'],
                                           coordinate['lon'])

    if inside_polygon_result is None:
        logging.info(msg=r.COORD_RANGE_WARNING)
        return {'message': r.COORD_RANGE_WARNING}, 500

    # If the given address is inside MKAD
    if inside_polygon_result:
        logging.info(msg=r.NO_NEED_CALCULATING)
        return {'message': r.NO_NEED_CALCULATING}, 200

    # Calculate distance between MKAD and the given address
    distance = calculate_distance(coordinate['lon'], coordinate['lat'])

    # Sometimes with OSRM API it is possbile to see server errors.
    if distance is None:
        logging.error(msg=r.SMTH_WENT_WRONG_OSRM)
        return {'message': r. SMTH_WENT_WRONG_OSRM}, 500

    response = {
        'from': 'Moscow Ring Road',
        'to': address,
        'distance': '{0:.3f}'.format(distance / 1000)
    }

    logging.info(msg=response)
    return response, 200
