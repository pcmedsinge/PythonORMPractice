# Setup and Run Guide

This guide gives end-to-end setup and execution commands for all phases.

## 1) Prerequisites
- Docker Desktop installed and running
- Python available (project currently validated with Python 3.14)
- PowerShell terminal

## 2) Start PostgreSQL (port 55432)
From workspace root:

```powershell
docker compose up -d
```

Optional check:

```powershell
docker ps --filter "name=python-orm-practice-postgres"
```

## 3) Create environment and install dependencies
Note: `uv` was not available on this machine during implementation, so commands below use `.venv` + `pip`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install sqlalchemy psycopg[binary] alembic sqlmodel fastapi uvicorn django dj-database-url python-dotenv
```

## 4) Create local env file (if missing)

```powershell
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
```

## 5) Django migration setup (required before Django phase scripts)

```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py makemigrations orm_lab
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py migrate
```

## 6) Run phase scripts
- SQLAlchemy phase commands: see `sqlalchemy-phases/RUN_PHASES.md`
- Django ORM phase commands: see `django-orm-phases/RUN_PHASES.md`
- SQLModel phase commands: see `sqlmodel-phases/RUN_PHASES.md`

## 7) Stop services

```powershell
docker compose down
```

## 8) Reset databases

```powershell
docker compose down -v
docker compose up -d
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py migrate
```
