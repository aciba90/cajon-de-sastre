# NBA Stats

## Description

Technest Python Tech Challenge solution.

Web App to compute statistic graphs from NBA data. The web framework used is FastAPI,
Gunicorn as server with Uvicorn workers.

## Start production server

To start the production server execute `docker-compose up -d` and access
[http://localhost:5000/nbastats](http://localhost:5000/nbastats)

To see the doc open [http://localhost:5000/docs](http://localhost:5000/docs) or
[http://localhost:5000/redoc](http://localhost:5000/redoc)

## Development

* To start up the development or production server run `make start[-prod]` respectively.

* To build them run `make build[-prod]`

* To execute linters run `make format lint`

* To execute the tests run `make test`
