.PHONY:

help:
	@echo "Доступные команды:"
	@echo "  make env       - Создать env из экземпляра"
	@echo "  make up        - Запустить контейнеры"
	@echo "  make down      - Остановить контейнеры"
	@echo "  make build     - Пересобрать образы"
	@echo "  make migrate   - Применить миграции БД"
	@echo "  make seed      - Загрузить тестовые данные"
	@echo "  make logs      - Показать логи приложения"
	@echo "  make shell     - Открыть shell в контейнере"
	@echo "  make clean     - Остановить и удалить volumes"
	@echo "  make restart   - Перезапустить контейнеры"

env:
	cp .env.example .env

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

migrate:
	docker compose exec app uv run alembic revision --autogenerate -m "Initial migration" || true
	docker compose exec app uv run alembic upgrade head

seed:
	docker compose exec app uv run python test_seed.py

logs:
	docker compose logs -f app

shell:
	docker compose exec app bash

clean:
	docker compose down -v

restart:
	docker compose restart app