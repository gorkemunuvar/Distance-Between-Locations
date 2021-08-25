from flask import Blueprint, request
from services.distance import DistanceService


distance_api = Blueprint('distance', __name__)


@distance_api.route('/', methods=['GET'])
def get_distance():
    address = request.args.get('address', None)

    print(f'Address: {address}')

    # handle it anyway
    if address is None:
        return {'message': 'address parameter can not be empty.'}

    distance = DistanceService.calculate_distance(address)

    if distance:
        return {'distance': distance}, 200
