from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from django.db import models, connection


class Campus(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        app_label = "orm_lab"
        managed = False
        db_table = "dj_lab_campus"


class Classroom(models.Model):
    label = models.CharField(max_length=120)
    campus_id = models.IntegerField()

    class Meta:
        app_label = "orm_lab"
        managed = False
        db_table = "dj_lab_classroom"


def ensure_tables() -> None:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS dj_lab_classroom")
        cursor.execute("DROP TABLE IF EXISTS dj_lab_campus")
        cursor.execute(
            "CREATE TABLE dj_lab_campus (id BIGSERIAL PRIMARY KEY, name VARCHAR(120) UNIQUE NOT NULL)"
        )
        cursor.execute(
            "CREATE TABLE dj_lab_classroom (id BIGSERIAL PRIMARY KEY, label VARCHAR(120) NOT NULL, campus_id BIGINT NOT NULL REFERENCES dj_lab_campus(id))"
        )


def main() -> None:
    ensure_tables()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO dj_lab_campus (name) VALUES ('North Campus'), ('South Campus')")
        cursor.execute(
            "INSERT INTO dj_lab_classroom (label, campus_id) VALUES ('N-101', 1), ('N-102', 1), ('S-201', 2)"
        )
        cursor.execute(
            "SELECT c.name, COUNT(r.id) FROM dj_lab_campus c LEFT JOIN dj_lab_classroom r ON c.id = r.campus_id GROUP BY c.name ORDER BY c.name"
        )
        rows = cursor.fetchall()

    for name, count in rows:
        print(name, count)

    print("Admin registration reference: see django-orm-phases/project/orm_lab/admin.py")


if __name__ == "__main__":
    main()
