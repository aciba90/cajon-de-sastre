
dev_stack_name = technest_dev
dev_compose_flags = -f docker-compose.yml -f docker-compose.dev.yml -p $(dev_stack_name)
src_path = app

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .mypy_cache/ .pytest_cache/

build:
	DOCKER_BUILDKIT=0 docker-compose $(dev_compose_flags) build

build-prod:
	DOCKER_BUILDKIT=0 docker-compose build

start:
	docker-compose $(dev_compose_flags) up

start-prod:
	docker-compose up

logs:
	docker-compose logs --follow

stop:
	docker-compose stop

cmd:
	docker-compose run -- web bash

lint:
	docker-compose $(dev_compose_flags) run -- web \
		python -m mypy --ignore-missing-imports -- $(src_path)
	docker-compose $(dev_compose_flags) run -- web \
		python -m flake8 --max-line-length 88 --extend-ignore E203 -- $(src_path)

format:
	docker-compose $(dev_compose_flags) run -- web python -m black -- $(src_path)

test:
	docker-compose $(dev_compose_flags) run -- web \
		python -m pytest --doctest-modules -vv -- $(src_path)
