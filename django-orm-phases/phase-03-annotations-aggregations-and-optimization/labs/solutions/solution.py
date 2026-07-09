from pathlib import Path
import sys
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[3] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from django.db import transaction
from django.db.models import Sum, Avg
from orm_lab.models import Revenue, Wallet


def transfer_credits(from_owner: str, to_owner: str, amount: Decimal) -> None:
    with transaction.atomic():
        source = Wallet.objects.select_for_update().get(owner=from_owner)
        target = Wallet.objects.select_for_update().get(owner=to_owner)
        if source.balance < amount:
            raise ValueError("Insufficient balance")
        source.balance = source.balance - amount
        target.balance = target.balance + amount
        source.save(update_fields=["balance"])
        target.save(update_fields=["balance"])


def main() -> None:
    Revenue.objects.all().delete()
    Wallet.objects.all().delete()

    Revenue.objects.bulk_create(
        [
            Revenue(category="books", amount=300),
            Revenue(category="books", amount=900),
            Revenue(category="courses", amount=500),
            Revenue(category="courses", amount=1500),
            Revenue(category="tools", amount=250),
        ]
    )

    Wallet.objects.bulk_create(
        [
            Wallet(owner="Rita", balance=500),
            Wallet(owner="Sahil", balance=100),
        ]
    )

    report = (
        Revenue.objects.values("category")
        .annotate(total_revenue=Sum("amount"), avg_revenue=Avg("amount"))
        .order_by("-total_revenue")
    )

    print("Revenue report:")
    for row in report:
        print(row["category"], float(row["total_revenue"]), round(float(row["avg_revenue"]), 2))

    try:
        transfer_credits("Rita", "Sahil", Decimal("120"))
        print("Transfer 1 success")
    except Exception as ex:
        print("Transfer 1 failed:", ex)

    try:
        transfer_credits("Sahil", "Rita", Decimal("2000"))
        print("Transfer 2 success")
    except Exception as ex:
        print("Transfer 2 failed:", ex)

    print("Final balances:")
    for w in Wallet.objects.order_by("owner"):
        print(w.owner, float(w.balance))


if __name__ == "__main__":
    main()
