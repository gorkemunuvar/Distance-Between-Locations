from flask import Flask
from flask_restful import Api
from resources.distance import Distance

app = Flask(__name__)
api = Api(app)


def set_api() -> None:
    api.add_resource(Distance, '/<string:address>')


if __name__ == '__main__':
    set_api()
    app.run(debug=True)
