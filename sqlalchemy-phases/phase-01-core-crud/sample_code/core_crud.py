import os
from sqlalchemy import String, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "sa_students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)


def main() -> None:
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(
            [
                Student(name="Asha", city="Pune"),
                Student(name="Rohan", city="Mumbai"),
                Student(name="Mira", city="Pune"),
            ]
        )
        session.commit()

        pune_students = session.scalars(
            select(Student).where(Student.city == "Pune").order_by(Student.name)
        ).all()

        for row in pune_students:
            print(f"{row.id}: {row.name} ({row.city})")


if __name__ == "__main__":
    main()
