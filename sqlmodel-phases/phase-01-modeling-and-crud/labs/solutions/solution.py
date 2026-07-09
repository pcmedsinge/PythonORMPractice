import os
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Course(SQLModel, table=True):
    __tablename__ = "sm_courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    duration_hours: int


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine, tables=[Course.__table__])
    SQLModel.metadata.create_all(engine, tables=[Course.__table__])

    with Session(engine) as session:
        session.add_all(
            [
                Course(title="Python Basics", duration_hours=12),
                Course(title="SQL Fundamentals", duration_hours=10),
                Course(title="ORM Deep Dive", duration_hours=16),
            ]
        )
        session.commit()

        orm_course = session.exec(select(Course).where(Course.title == "ORM Deep Dive")).first()
        if orm_course:
            orm_course.duration_hours = 18
            session.add(orm_course)

        sql_course = session.exec(select(Course).where(Course.title == "SQL Fundamentals")).first()
        if sql_course:
            session.delete(sql_course)

        session.commit()

        rows = session.exec(select(Course).order_by(Course.title)).all()
        for row in rows:
            print(row.title, row.duration_hours)


if __name__ == "__main__":
    main()
