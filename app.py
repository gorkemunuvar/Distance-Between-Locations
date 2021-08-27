import logging
from flask import Flask

from config import SECRET_KEY
from blueprints.distance import distance_api

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(distance_api, url_prefix='/distance')

# This line creates a log file.
logging.basicConfig(filename='logs.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


@app.route('/', methods=['GET'])
def index():
    return {
        'message': 'Welcome to Distance Calculator'
    }, 200


@app.errorhandler(404)
def url_not_found(e):
    return {'Error': 'URL not found.'}, 404


if __name__ == '__main__':
    app.run(debug=True)
