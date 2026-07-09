from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from orm_lab.models import Department, Employee


def main() -> None:
    Department.objects.all().delete()

    eng = Department.objects.create(name="Engineering")
    ops = Department.objects.create(name="Operations")

    Employee.objects.bulk_create(
        [
            Employee(name="Nina", department=eng),
            Employee(name="Arun", department=eng),
            Employee(name="Kabir", department=ops),
        ]
    )

    for dep in Department.objects.all().order_by("name"):
        print(dep.name, list(dep.employees.values_list("name", flat=True)))


if __name__ == "__main__":
    main()
