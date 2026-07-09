import os
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Author(SQLModel, table=True):
    __tablename__ = "sm_authors"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    books: List["Book"] = Relationship(back_populates="author")


class Book(SQLModel, table=True):
    __tablename__ = "sm_books"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="sm_authors.id")
    author: Optional[Author] = Relationship(back_populates="books")


class StudentClubLink(SQLModel, table=True):
    __tablename__ = "sm_student_club"

    student_id: Optional[int] = Field(default=None, foreign_key="sm_students.id", primary_key=True)
    club_id: Optional[int] = Field(default=None, foreign_key="sm_clubs.id", primary_key=True)


class Student(SQLModel, table=True):
    __tablename__ = "sm_students"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    clubs: List["Club"] = Relationship(back_populates="students", link_model=StudentClubLink)


class Club(SQLModel, table=True):
    __tablename__ = "sm_clubs"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    students: List[Student] = Relationship(back_populates="clubs", link_model=StudentClubLink)


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        a1 = Author(name="Priya")
        a2 = Author(name="Karan")
        session.add_all([a1, a2])
        session.commit()
        session.refresh(a1)
        session.refresh(a2)

        session.add_all(
            [
                Book(title="Pragmatic ORM", author_id=a1.id),
                Book(title="Modern APIs", author_id=a1.id),
                Book(title="Data Platforms", author_id=a2.id),
            ]
        )

        s1 = Student(name="Aditi")
        s2 = Student(name="Rahul")
        c1 = Club(name="Math")
        c2 = Club(name="Music")
        s1.clubs.extend([c1, c2])
        s2.clubs.append(c1)

        session.add_all([s1, s2, c1, c2])
        session.commit()

        priya_books = session.exec(select(Book).join(Author).where(Author.name == "Priya")).all()
        print("Priya books:", [b.title for b in priya_books])

        aditi = session.exec(select(Student).where(Student.name == "Aditi")).first()
        if aditi:
            print("Aditi clubs:", [c.name for c in aditi.clubs])

        math = session.exec(select(Club).where(Club.name == "Math")).first()
        if math:
            print("Math members:", [s.name for s in math.students])


if __name__ == "__main__":
    main()
