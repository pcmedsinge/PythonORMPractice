# Django ORM Phase Run Instructions

Run from workspace root `E:\PracticeApps\PythonRelated\PythonSqlORMFrameworks\PythonORMPractice`.

## One-time setup for Django track
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py makemigrations orm_lab
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py migrate
```

## Phase 01: Models and Admin
### Sample code
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-01-models-and-admin\sample_code\models_crud_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-01-models-and-admin\labs\solutions\solution.py
```

## Phase 02: QuerySets and Relations
### Sample code
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-02-querysets-and-relations\sample_code\relations_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-02-querysets-and-relations\labs\solutions\solution.py
```

## Phase 03: Annotations, Aggregations, Optimization
### Sample code
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-03-annotations-aggregations-and-optimization\sample_code\analytics_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-03-annotations-aggregations-and-optimization\labs\solutions\solution.py
```

## Phase 04: Migrations, Signals, Mini Project
### Sample code
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-04-migrations-signals-and-mini-project\sample_code\mini_project_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\phase-04-migrations-signals-and-mini-project\labs\solutions\solution.py
```

## Optional: run Django admin site
```powershell
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py createsuperuser
.\.venv\Scripts\python.exe .\django-orm-phases\project\manage.py runserver
```
