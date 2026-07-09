from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from django.db.models import Sum, Avg
from orm_lab.models import Revenue


def main() -> None:
    Revenue.objects.all().delete()
    Revenue.objects.bulk_create(
        [
            Revenue(category="books", amount=400),
            Revenue(category="books", amount=700),
            Revenue(category="courses", amount=1200),
            Revenue(category="courses", amount=800),
        ]
    )

    report = (
        Revenue.objects.values("category")
        .annotate(total_revenue=Sum("amount"), avg_revenue=Avg("amount"))
        .order_by("-total_revenue")
    )

    for row in report:
        print(row["category"], float(row["total_revenue"]), float(row["avg_revenue"]))


if __name__ == "__main__":
    main()
