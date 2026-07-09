import os
from sqlalchemy import String, Integer, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "sa_courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=False)


def main() -> None:
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.drop_all(engine, tables=[Course.__table__])
    Base.metadata.create_all(engine, tables=[Course.__table__])

    with Session(engine) as session:
        session.add_all(
            [
                Course(title="Python Basics", duration_hours=12),
                Course(title="SQL Fundamentals", duration_hours=10),
                Course(title="ORM Deep Dive", duration_hours=16),
            ]
        )
        session.commit()

        rows = session.scalars(select(Course).order_by(Course.title)).all()
        print("Initial rows:")
        for row in rows:
            print(row.title, row.duration_hours)

        total = session.scalar(select(func.count()).select_from(Course))
        print("Total:", total)

        orm = session.scalar(select(Course).where(Course.title == "ORM Deep Dive"))
        if orm:
            orm.duration_hours = 18

        sql_f = session.scalar(select(Course).where(Course.title == "SQL Fundamentals"))
        if sql_f:
            session.delete(sql_f)

        session.commit()

        final_rows = session.scalars(select(Course).order_by(Course.title)).all()
        print("Final rows:")
        for row in final_rows:
            print(row.title, row.duration_hours)


if __name__ == "__main__":
    main()
