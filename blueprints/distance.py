import logging
from flask import Blueprint, request
from services.geocoding import get_coordinate
from services.point_polygon import in_polygon
from services.distance import calculate_distance, calculate_distance_gh


distance_api = Blueprint('distance', __name__)


@distance_api.route('/', methods=['GET'])
def get_distance():
    params = request.args
    address = params.get('address', None)

    if address is None:
        return {'message': '<address> parameter is missing.'}

    coordinate = get_coordinate(address.lower())

    if coordinate is None:
        logging.error(msg='Make sure that address information is correct.')

        return {
            'message': 'Make sure that address information is correct.'
        }, 500

    in_polygon_result = in_polygon(coordinate['lat'], coordinate['lon'])

    if in_polygon_result is None:
        msg = 'Valid latitude range(-90, 90), Valid longitude range(-180, 180)'
        logging.info(msg=msg)

        return {'message': msg}, 500

    if in_polygon_result:
        msg = 'No need to calculate. Address is already in Moscow Ring Road.'
        logging.info(msg=msg)

        return {'message': msg}, 200

    # Points were gotten from the link below
    # https://www.coordinatesfinder.com/coordinates
    # /810957-66-km-mkad-moscow-russia
    source_lon = 37.3903193
    source_lat = 55.8142861
    target_lon = coordinate['lon']
    target_lat = coordinate['lat']

    distance = 0
    use_graphhopper = params.get('use_graphhopper', None)

    if use_graphhopper:
        distance = calculate_distance_gh(source_lon, source_lat,
                                         target_lon, target_lat)

        if distance is None:
            logging.error(
                msg='While calculating distance with GRAPHHOPPER')

            return {
                'message': 'Something went wrong while calculating distance.'
            }, 500

    else:
        distance = calculate_distance(source_lon, source_lat,
                                      target_lon, target_lat)

        if distance is None:
            logging.error(msg='While calculating distance with OSRM.')

            return {
                'message': '''Somehting went wrong while calculating distance. 
                              Try <use_graph_hopper>  query parameter to use
                              GRAPHHOPPER Routing Machine for calculating instead '''
            }, 500

    response = {
        'from': 'Moscow Ring Road',
        'to': address,
        'distance': '{0:.3f}'.format(distance / 1000)
    }

    logging.info(msg=response)

    return response, 200
