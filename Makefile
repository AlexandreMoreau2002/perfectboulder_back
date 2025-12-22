.PHONY: up down logs shell

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec backend /bin/bash

lint:
	docker compose exec backend python -m ruff check app
