# Distance-Between-Locations

This API allows you to calculate distance as km. between the address you specified and Moscow Ring Road if the given address is not inside Moscow Ring Road.

For creating the API Flask web framework was used.

## Dependencies

This projects uses `pipenv` as a virtual environment. Make sure that you have pipenv installed in your machine.

### Virtual Environment

If you don't have pipenv install on your machine:

For Windows, run:

```
pip install --user pipenv
```

For others, check it out the docs from [here](https://github.com/pypa/pipenv).

### Installing Dependencies

Run:

```
pipenv install
```

or if there are dev dependencies, run:

```
pipenv install --dev
```



## How to Run

You should run the `app.py` using the command below:

```
python app.py
```

If you are running the applicaiton on your local machine do not forget that Flask uses `port: 5000` as default.
Your endpoint would be like:

`http://localhost:5000`

## Running Tests

There are a set of unit tests in `/tests` folder.

Running test for the services(functions):
```
python -m unittest tests.test_services -v
```

Running test for the API:
```
python -m unittest tests.test_api -v
```

If all tests are passed, you won't have any problem while working or using the API.

`DON'T` forget it is possbible to see server errors while getting distance using OSRM API
because it is open source and not suitible for production.

## Creating Docker Image and Docker Container

You sould firstly make sure that you have Docker installed on your machine.

To create a Docker image, run:

```
docker build -t <your image name>:latest .
```

To create a docker container from the Docker image, run:

```
docker run -it <your image name>
```
### Note

Docker iamge size can be smaller with implementing a ray casting algorithm to check if a point is insdide a polygon. But in this project `shapely` module used.


# Docs

There are some example responses here but all the API documentation created by POSTMAN can be found in the link below.

https://documenter.getpostman.com/view/10919248/TzzHkYFH


## OVERVIEW

Here is the stesps how the API works in the backgrond.

#### 1. Geocoding

You should firstly give a valid address information to the API and then API converts the address into a coordinate that includes latitude and longitude information using Yandex Map Gecocoding API.

#### 2. Check if the given address is aldready inside Moscow Ring Road.
 
Once the coordinate is grabbed for the given address API checks if the given point(coordinate) is inside the polygon(Moscow Ring Road boundries).

#### 3. Calculating Distance

If the coordinate for the given address is not inside Moscow Ring Road, then API calculates the distance from Moscow Ring Road to the specified address using OSRM API (Open Street Routing Machine).


## Error Codes

 - 200: When the response is ok.
 - 400: When the address parameter is missing or invalid address info.
 - 404: URL not found.
 - 500: When something unexpected occurs.

## Example

You can make a request to this endpoint:

`localhost:5000/distance?address=İstanbul`

When the API returns the response that includes distance correctly it looks like this.

    {
      "distance": "2341.655",
      "from": "Moscow Ring Road",
      "to": "istanbul"
    }

In the response body distance value is kilometer(km).

### Note

It is rarerly possible to see 500 server errors while getting the distance using the OSRM API because it is open source and not suitible for production.
The reason that I did not use Yandex Routing Machine, it was not free.


## For more

https://documenter.getpostman.com/view/10919248/TzzHkYFH
