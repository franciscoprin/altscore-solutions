.PHONY: build up down logs test test-verbose fmt

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

test:
	docker compose run --rm nave-a-la-deriva pytest -q

test-verbose:
	docker compose run --rm nave-a-la-deriva pytest -vv
