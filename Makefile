
NAME = some-mysql

run:
	docker-compose -f stack.yml up

bash:
	docker-compose -f stack.yml exec -u root -p - db bash

