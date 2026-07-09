# Verification Commands

Run from workspace root.

## Start services
- docker compose up -d

## Django migration
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\project\\manage.py makemigrations orm_lab
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\project\\manage.py migrate

## SQLAlchemy solved labs
- .\\.venv\\Scripts\\python.exe .\\sqlalchemy-phases\\phase-01-core-crud\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\sqlalchemy-phases\\phase-02-relationships-and-joins\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\sqlalchemy-phases\\phase-03-advanced-querying-and-transactions\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\sqlalchemy-phases\\phase-04-migrations-and-mini-project\\labs\\solutions\\solution.py

## Django solved labs
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\phase-01-models-and-admin\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\phase-02-querysets-and-relations\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\phase-03-annotations-aggregations-and-optimization\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\django-orm-phases\\phase-04-migrations-signals-and-mini-project\\labs\\solutions\\solution.py

## SQLModel solved labs
- .\\.venv\\Scripts\\python.exe .\\sqlmodel-phases\\phase-01-modeling-and-crud\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\sqlmodel-phases\\phase-02-relationships-and-query-patterns\\labs\\solutions\\solution.py
- .\\.venv\\Scripts\\python.exe .\\sqlmodel-phases\\phase-04-migrations-and-mini-project\\labs\\solutions\\solution.py

## SQLModel FastAPI syntax checks
- .\\.venv\\Scripts\\python.exe -m py_compile .\\sqlmodel-phases\\phase-03-fastapi-integration-basics\\sample_code\\app.py
- .\\.venv\\Scripts\\python.exe -m py_compile .\\sqlmodel-phases\\phase-03-fastapi-integration-basics\\labs\\solutions\\solution.py
