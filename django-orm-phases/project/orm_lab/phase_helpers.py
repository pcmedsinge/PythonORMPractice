import os
import django


def setup_django() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_practice.settings")
    django.setup()
