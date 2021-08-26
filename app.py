import logging
from flask import Flask

from config import SECRET_KEY
from blueprints.distance import distance_api

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(distance_api, url_prefix='/distance')

logging.basicConfig(filename='logs.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Distance Calculator', 200


if __name__ == '__main__':
    app.run(debug=True)
