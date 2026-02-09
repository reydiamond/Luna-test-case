help:
	@echo "Команды для разработки:"
	@echo "  make env     - Создать .env"
	@echo "  make up        - Запустить все сервисы"
	@echo "  make down      - Остановить все сервисы"
	@echo "  make migrate   - Применить миграции Alembic"
	@echo "  make seed      - Заполнить БД тестовыми данными"
	@echo "  make app       - Запустить приложение"


env:
	cp -n .env.example .env || true

up:
	docker compose up -d postgres

down:
	docker compose down

migrate:
	docker compose exec app uv run alembic -c migrations/alembic.ini upgrade head

seed:
	docker compose exec app uv run python test_seed.py

app:
	docker compose up -d app
