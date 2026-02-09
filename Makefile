UV = uv run

help:
	@echo "Команды для разработки:"
	@echo "  make up        - Запустить Postgres (Docker)"
	@echo "  make down      - Остановить Postgres (и удалить контейнер)"
	@echo "  make migrate   - Применить миграции Alembic"
	@echo "  make seed      - Заполнить тестовыми данными"
	@echo "  make app       - Запустить приложение (uvicorn через uv)"


up:
	docker compose up -d postgres

down:
	docker compose down

migrate:
	$(UV) alembic upgrade head

seed:
	$(UV) python test_seed.py

app:
	$(UV) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
