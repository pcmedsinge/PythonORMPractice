# SQLModel Phase Run Instructions

Run from workspace root `E:\PracticeApps\PythonRelated\PythonSqlORMFrameworks\PythonORMPractice`.

## Phase 01: Modeling and CRUD
### Sample code
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-01-modeling-and-crud\sample_code\crud_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-01-modeling-and-crud\labs\solutions\solution.py
```

## Phase 02: Relationships and Query Patterns
### Sample code
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-02-relationships-and-query-patterns\sample_code\relationships_sample.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-02-relationships-and-query-patterns\labs\solutions\solution.py
```

## Phase 03: FastAPI Integration Basics
### Sample code API (run server)
```powershell
.\.venv\Scripts\python.exe -m uvicorn sqlmodel-phases.phase-03-fastapi-integration-basics.sample_code.app:app --reload
```

### Lab solution API (run server)
```powershell
.\.venv\Scripts\python.exe -m uvicorn sqlmodel-phases.phase-03-fastapi-integration-basics.labs.solutions.solution:app --reload
```

### API quick checks
- Open: http://127.0.0.1:8000/docs
- Use Swagger UI to test POST/GET endpoints

## Phase 04: Migrations and Mini Project
### Sample code
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-04-migrations-and-mini-project\sample_code\mini_project.py
```

### Lab solution
```powershell
.\.venv\Scripts\python.exe .\sqlmodel-phases\phase-04-migrations-and-mini-project\labs\solutions\solution.py
```

## Optional syntax checks for phase 03
```powershell
.\.venv\Scripts\python.exe -m py_compile .\sqlmodel-phases\phase-03-fastapi-integration-basics\sample_code\app.py
.\.venv\Scripts\python.exe -m py_compile .\sqlmodel-phases\phase-03-fastapi-integration-basics\labs\solutions\solution.py
```
