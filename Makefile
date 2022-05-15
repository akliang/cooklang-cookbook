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
	@export UID=${CURRENT_UID}; export GID=${CURRENT_GID}; docker-compose up -d

down: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose down

test:
	@docker-compose run api python3 manage.py test

conn-api:
	@docker exec -it cooklang-cookbook_api_1 bash

conn-db:
	@docker exec -it cooklang-cookbook_db_1 bash

docker-login:
	@docker login docker.io -u $$DOCKER_USERNAME -p $$DOCKER_PASSWORD

docker-logout:
	@docker logout docker.io

docker-push:
	@docker push akliang/cookbook_api:latest
	@docker push akliang/cookbook_api:latest
