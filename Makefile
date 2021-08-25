
NAME = some-mysql

build:
	docker-compose build

run:
	docker-compose up

bash:
	docker-compose exec db bash
	
mysql:
	docker-compose exec db mysql -u root -p
