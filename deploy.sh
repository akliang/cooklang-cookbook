#!/bin/bash

TAG="$1"

# check if the env file needs updating
EXPWC=$( wc -l .env.example | awk '{ print $1 }')
ENVWC=$( wc -l .env | awk '{ print $1 }')
if [[ "$EXPWC" != "$ENVWC" ]]; then
  echo ".env.example (wc $EXPWC) and .env (wc $ENVWC) files do not match, please double check"
  exit
fi

# bring down old containers
make down

# rebase main branch
git pull

# switch to requested release branch
git checkout "$TAG"

# launch containers
make up-d

# run Django migration
make migrate-prod