# Running too many tests in parallel exhausts shared memory on some machines
MAXPROC ?= 16

up:
	scripts/up.sh

build:
	scripts/local_build.sh

shell:
	docker-compose exec server pipenv run /bin/bash

clean:
	docker-compose exec server pipenv run /app/ops/dev/clean.sh

mypy:
	docker-compose exec server pipenv run mypy /app/

migrate:
	docker-compose exec server pipenv run /app/manage.py migrate

createsuperuser:
	docker-compose exec server pipenv run /app/manage.py createsuperuser
