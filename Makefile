up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	pytest -q

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(m)"