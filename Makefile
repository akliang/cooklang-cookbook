#!make
include .env
export $(shell sed 's/=.*//' .env)

build: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose build

build-no-cache:
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose build --no-cache

up: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose up

up-d:
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose up -d

down: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose down

test:
	@docker-compose run api python3 manage.py test api.tests.test_authentication_views

conn-db:
	@docker exec -it cooklang-cookbook_db_1 bash

conn-db-prod:
	@docker exec -it cooklang-cookbook-prod_db_1 bash

migrate:
	@docker exec -it cooklang-cookbook_api_1 python3 manage.py migrate

migrate-prod:
	@docker exec -it cooklang-cookbook-prod_api_1 python3 manage.py migrate

docker-login:
	@docker login docker.io -u $$DOCKER_USERNAME -p $$DOCKER_PASSWORD

docker-logout:
	@docker logout docker.io

docker-push:
	@docker push akliang/cookbook_api:latest
	@docker push akliang/cookbook_api:latest
