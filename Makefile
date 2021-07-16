build:
	DOCKER_BUILDKIT=0 docker-compose build

build-prod:
	DOCKER_BUILDKIT=0 docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

start:
	docker-compose up

start-prod:
	docker-compose -f docker-compose.yml up

logs:
	docker-compose logs --follow

stop:
	docker-compose stop

cmd:
	docker-compose run web bash

lint:
	docker-compose run web python -m mypy --ignore-missing-imports -- app
	docker-compose run web python -m flake8 --max-line-length 88 --extend-ignore E203 -- app

format:
	docker-compose run web python -m black -- app
