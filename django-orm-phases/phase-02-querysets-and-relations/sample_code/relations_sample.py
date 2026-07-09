from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from orm_lab.models import Author, Book, Club, Student


def main() -> None:
    Book.objects.all().delete()
    Author.objects.all().delete()
    Student.objects.all().delete()
    Club.objects.all().delete()

    a1 = Author.objects.create(name="Leena")
    a2 = Author.objects.create(name="Dev")
    Book.objects.bulk_create(
        [
            Book(title="Data Story", author=a1),
            Book(title="Analytics 101", author=a1),
            Book(title="APIs for Teams", author=a2),
        ]
    )

    c1 = Club.objects.create(name="Robotics")
    c2 = Club.objects.create(name="Drama")
    s1 = Student.objects.create(name="Ira")
    s2 = Student.objects.create(name="Manav")
    s1.clubs.add(c1, c2)
    s2.clubs.add(c1)

    books = Book.objects.select_related("author").filter(author__name="Leena")
    print("Books by Leena:", [b.title for b in books])

    robotics = Club.objects.prefetch_related("students").get(name="Robotics")
    print("Robotics members:", [s.name for s in robotics.students.all()])


if __name__ == "__main__":
    main()
