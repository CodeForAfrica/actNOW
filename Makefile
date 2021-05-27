COMPOSE = docker-compose
COMPOSE_BUILD_ENV = COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1
COMPOSE_BUILD_FLAGS = --progress=plain

build:
	$(COMPOSE_BUILD_ENV) $(COMPOSE) build $(COMPOSE_BUILD_FLAGS)

run:
	$(COMPOSE_BUILD_ENV) $(COMPOSE) up -d

enter:
	$(COMPOSE) exec app bash

createsuperuser:
	$(COMPOSE) exec app python manage.py createsuperuser

isort:
	$(COMPOSE) exec -t app isort .

black:
	$(COMPOSE) exec -t app black .

flake8:
	$(COMPOSE) exec -t app flake8 --exclude venv

mypy:
	$(COMPOSE) exec -t app mypy . --ignore-missing-imports

test:
	$(COMPOSE) exec -t app python manage.py test

stop:
	$(COMPOSE) down
