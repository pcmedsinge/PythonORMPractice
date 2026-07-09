# Quickstart

## Prerequisites
- Docker Desktop
- uv installed
- Git

## 1) Start PostgreSQL
From workspace root:

powershell
  docker compose up -d

Validate container health:

powershell
  docker ps --filter "name=python-orm-practice-postgres"

## 2) Create environment with uv

powershell
  uv venv .venv
  .\.venv\Scripts\Activate.ps1

## 3) Install common and track dependencies

powershell
  uv pip install sqlalchemy psycopg[binary] alembic sqlmodel fastapi pydantic
  uv pip install django dj-database-url

## 4) Configure environment variables
Copy .env.example to .env and adjust if needed.

## 5) Start learning
- SQLAlchemy: sqlalchemy-phases/
- Django ORM: django-orm-phases/
- SQLModel: sqlmodel-phases/

## 6) Stop services

powershell
  docker compose down

## 7) Reset databases

powershell
  docker compose down -v
  docker compose up -d
