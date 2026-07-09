import os
from sqlalchemy import String, Integer, ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, selectinload

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "sa_departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class Employee(Base):
    __tablename__ = "sa_employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("sa_departments.id"))
    department: Mapped[Department] = relationship(back_populates="employees")


def main() -> None:
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.drop_all(engine, tables=[Employee.__table__, Department.__table__])
    Base.metadata.create_all(engine, tables=[Department.__table__, Employee.__table__])

    with Session(engine) as session:
        eng = Department(name="Engineering")
        ops = Department(name="Operations")
        session.add_all([eng, ops])
        session.flush()

        session.add_all(
            [
                Employee(name="Nina", department_id=eng.id),
                Employee(name="Arun", department_id=eng.id),
                Employee(name="Kabir", department_id=ops.id),
            ]
        )
        session.commit()

        rows = session.scalars(
            select(Department).options(selectinload(Department.employees)).order_by(Department.name)
        ).all()
        for dept in rows:
            print(dept.name, [e.name for e in dept.employees])


if __name__ == "__main__":
    main()
