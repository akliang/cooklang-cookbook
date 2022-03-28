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