from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from django.db.models import Sum
from orm_lab.models import ClinicPatient, Appointment


def main() -> None:
    Appointment.objects.all().delete()
    ClinicPatient.objects.all().delete()

    p1 = ClinicPatient.objects.create(name="Anita")
    p2 = ClinicPatient.objects.create(name="Kunal")

    Appointment.objects.bulk_create(
        [
            Appointment(patient=p1, fee=1200, status="completed"),
            Appointment(patient=p1, fee=800, status="completed"),
            Appointment(patient=p2, fee=1000, status="completed"),
        ]
    )

    report = (
        Appointment.objects.values("patient__name")
        .annotate(total_fee=Sum("fee"))
        .order_by("-total_fee")
    )
    for row in report:
        print(row["patient__name"], float(row["total_fee"]))


if __name__ == "__main__":
    main()
