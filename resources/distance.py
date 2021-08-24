from flask_restful import Resource
from services.distance import DistanceService


class Distance(Resource):
    @classmethod
    def get(cls, address):
        print('yo')

        distance = DistanceService.calculate_distance(address)

        if distance:
            return {'distance': distance}, 200
