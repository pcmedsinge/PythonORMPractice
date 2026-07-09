import os
from sqlalchemy import String, Integer, ForeignKey, Table, Column, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


student_club = Table(
    "sa_student_club",
    Base.metadata,
    Column("student_id", ForeignKey("sa_students_rel.id"), primary_key=True),
    Column("club_id", ForeignKey("sa_clubs.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "sa_authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "sa_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    author_id: Mapped[int] = mapped_column(ForeignKey("sa_authors.id"))
    author: Mapped[Author] = relationship(back_populates="books")


class Student(Base):
    __tablename__ = "sa_students_rel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    clubs: Mapped[list["Club"]] = relationship(secondary=student_club, back_populates="students")


class Club(Base):
    __tablename__ = "sa_clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    students: Mapped[list[Student]] = relationship(secondary=student_club, back_populates="clubs")


def main() -> None:
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        a1 = Author(name="Leena")
        a2 = Author(name="Dev")
        session.add_all([a1, a2])
        session.flush()

        session.add_all(
            [
                Book(title="Data Story", author_id=a1.id),
                Book(title="Analytics 101", author_id=a1.id),
                Book(title="APIs for Teams", author_id=a2.id),
                Book(title="Scaling Systems", author_id=a2.id),
            ]
        )

        s1 = Student(name="Ira")
        s2 = Student(name="Manav")
        c1 = Club(name="Robotics")
        c2 = Club(name="Drama")

        s1.clubs.extend([c1, c2])
        s2.clubs.append(c1)
        session.add_all([s1, s2, c1, c2])
        session.commit()

        authors = session.scalars(
            select(Author).options(selectinload(Author.books)).order_by(Author.name)
        ).all()
        for author in authors:
            print(author.name, [b.title for b in author.books])

        books_for_leena = session.scalars(
            select(Book).join(Book.author).where(Author.name == "Leena")
        ).all()
        print("Books by Leena:", [b.title for b in books_for_leena])

        robotics = session.scalar(select(Club).where(Club.name == "Robotics"))
        if robotics:
            print("Robotics members:", [s.name for s in robotics.students])

        ira = session.scalar(select(Student).where(Student.name == "Ira"))
        if ira:
            print("Ira clubs:", [c.name for c in ira.clubs])


if __name__ == "__main__":
    main()
