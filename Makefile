
NAME = some-mysql

build:
	docker-compose build

run:
	docker-compose up

bash:
	docker-compose exec db bash
	
mysql:
	docker-compose exec db mysql -u root -p

init-db:
	docker-compose exec -it db mysql -uroot -pexample < /sakila-db/sakila-schema.sql
	mysql -uroot -pexample < /sakila-db/sakila-data.sql
