# ---- Settings ----
PYTHON ?= python3
DJANGO_SETTINGS_MODULE ?= config.settings
MANAGE ?= $(PYTHON) manage.py
CODE_DIRS ?= apps config


# ---- linter commands ----
lint-fix:
	ruff check $(CODE_DIRS) --fix --unsafe-fixes

format:
	black $(CODE_DIRS)
	ruff check $(CODE_DIRS) --select I --fix

types:
	mypy $(CODE_DIRS)

security:
	bandit -q -r $(CODE_DIRS) -x "**/migrations/*,**/tests/*,tests/*"

check-django:
	$(MANAGE) check --settings=$(DJANGO_SETTINGS_MODULE)

lint-fix-all:
	$(MAKE) lint-fix
	$(MAKE) format
	$(MAKE) security
	$(MAKE) check-django
	@echo "✅ All linters done"

ruff-clean:
	ruff clean

# ---- docker commands ----
up:
	docker compose up -d

up-build:
	docker compose up -d --build

restart:
	docker compose restart

down:
	docker compose down

sh:
	docker compose exec web bash

test:
	docker compose exec web pytest

logs:
	docker compose logs

# ---- virtual environment commands ----
create-venv:
	python3 -m venv .venv

activate-venv:
	source .venv/bin/activate