build:
	DOCKER_BUILDKIT=0 docker-compose build

start:
	docker-compose up

logs:
	docker-compose logs --follow

stop:
	docker-compose stop
