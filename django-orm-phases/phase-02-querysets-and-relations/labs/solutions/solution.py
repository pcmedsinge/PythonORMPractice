from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3] / "project"
sys.path.insert(0, str(PROJECT_ROOT))

from orm_lab.phase_helpers import setup_django

setup_django()

from orm_lab.models import Author, Book, Club, Student


def main() -> None:
    Book.objects.all().delete()
    Author.objects.all().delete()
    Student.objects.all().delete()
    Club.objects.all().delete()

    a1 = Author.objects.create(name="Priya")
    a2 = Author.objects.create(name="Karan")

    Book.objects.bulk_create(
        [
            Book(title="Pragmatic ORM", author=a1),
            Book(title="Modern APIs", author=a1),
            Book(title="Data Platforms", author=a2),
            Book(title="Distributed Design", author=a2),
        ]
    )

    s1 = Student.objects.create(name="Aditi")
    s2 = Student.objects.create(name="Rahul")
    c1 = Club.objects.create(name="Math")
    c2 = Club.objects.create(name="Music")

    s1.clubs.add(c1, c2)
    s2.clubs.add(c1)

    priya_books = Book.objects.select_related("author").filter(author__name="Priya")
    print("Priya books:", [b.title for b in priya_books])

    aditi = Student.objects.prefetch_related("clubs").get(name="Aditi")
    print("Aditi clubs:", [c.name for c in aditi.clubs.all()])

    math_club = Club.objects.prefetch_related("students").get(name="Math")
    print("Math members:", [s.name for s in math_club.students.all()])


if __name__ == "__main__":
    main()
