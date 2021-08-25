from turtle import distance
from flask import Flask
from config import SECRET_KEY
from blueprints.distance import distance_api

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.register_blueprint(distance_api)

if __name__ == '__main__':
    app.run(debug=True)
