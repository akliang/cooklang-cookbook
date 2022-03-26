build: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose build

up: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose up

up-d:
	@export UID=${CURRENT_UID}; export GID=${CURRENT_GID}; docker-compose up -d

down: 
	@USERID=$(id -u) GROUPID=$(id -g) docker-compose down

test:
	@docker-compose run web python3 manage.py test