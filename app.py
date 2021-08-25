from turtle import distance
from flask import Flask
from blueprints.distance import distance_api

app = Flask(__name__)

app.register_blueprint(distance_api)

if __name__ == '__main__':
    app.run(debug=True)
