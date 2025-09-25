# Url Shortener Api

This application is a URL shortener service built with Django, Django Rest Framework and PostgreSQL, 
containerized using Docker. Provides a RESTful API for retrieving shortened URLs in both ways. 
Includes comprehensive testing and linting setup. Is well documented by docstrings, type hints, OpenAPI 
schema with Swagger UI, clear project structure and a Makefile with useful shortcuts.


[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg)](#)
[![Django](https://img.shields.io/badge/Django-5.2.6-092E20.svg)](#)
[![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.16.1-ff1709.svg)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](#)
[![Docker](https://img.shields.io/badge/Docker-✓-2496ED.svg)](#)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF.svg)](#)
---

## Table of Contents

* [Tech Stack](#tech-stack)
* [Makefile Shortcuts](#makefile-shortcuts)
* [Local Development](#local-development)
* [Available Endpoints](#available-endpoints)
* [Testing the API](#testing-the-api)
* [Brief Project Structure](#project-structure)

---

## Tech Stack

* **Backend:** Python 3.12, Django 5.2.6, Django Rest Framework 3.16.1
* **Database:** PostgreSQL 16+
* **Containerization:** Docker, docker‑compose
* **Tests:** pytest + pytest‑django,
* **Lint/format:** ruff, black, mypy, bandit, django check
---

## Makefile Shortcuts

```Makefile
up             # docker compose up -d
up-build       # docker compose up -d --build
restart        # docker compose restart
down           # docker compose down
sh             # docker compose exec web bash
test           # docker compose exec web pytest
logs           # docker compose logs
lint-fix-all   # ruff, black, bandit, django check
types          # mypy
create-venv    # python3 -m venv .venv
activate-venv  # source venv/bin/activate
```
---

## Local Development

### Prerequisites

* Docker Desktop / Engine 24+
* Python 3.12+
* Make (optional but recommended)

### Quickstart

```bash
make create-venv      # Create a virtual environment
make activate-venv    # Activate the virtual environment
cp .env.example .env  # Copy example env file
make up-build         # Build and start services, migrations will apply automatically
```

### Localhost Access

All endpoints are exposed once the application is running locally on:  
`http://localhost:8000/`  
`http://127.0.0.1:8000/`

---

## Available Endpoints
API endpoints are well documented under the `api/docs/` endpoint using Swagger UI.  
You can find them on local host under the following link: `http://localhost:8000/api/docs/`

---
## Testing the API

### Create a shortened URL
In order to create a shortened URL, you need to send a POST request to the `/shortener/` 
endpoint with the original URL in the request body. 
The response will include the shortened URL and its unique short code.

**Example local URL**
```
POST http://localhost:8000/shortener/
```

**Example Request Body**
```json
{
  "original_url": "https://example.com/some/long/long/very-long/path"
}
```
**Example local Response body**
```json
{
  "id": 0,
  "original_url": "https://example.com/some/long/long/very-long/path",
  "short_code": "ps0G7MT1ql",
  "short_url": "http://localhost:8000/ps0G7MT1ql"
}
```

### Resolve a shortened URL
In order to resolve a shortened URL back to its original URL, you need to send a GET request 
to the `/shortener/{short_code}/` endpoint, where `{short_code}` is the unique code of the shortened URL 
you want to resolve. The response will include the original URL associated with the provided short code.

**Example local URL**
```
GET http://localhost:8000/shortener/ps0G7MT1ql/
```
**Example local Response body**
```json
{
  "id": 0,
  "original_url": "https://example.com/some/long/long/very-long/path",
  "short_code": "ps0G7MT1ql"
}
```
---

## Brief Project Structure

```plaintext
.
├── apps/
│   ├── shortener/
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── apps.py
│       └── models.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .venv/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── Makefile
├── manage.py
├── pyproject.toml
├── README.md
└── requirements.txt
```