import os
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Learner(SQLModel, table=True):
    __tablename__ = "sm_learners"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    city: str


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine, tables=[Learner.__table__])
    SQLModel.metadata.create_all(engine, tables=[Learner.__table__])

    with Session(engine) as session:
        session.add_all(
            [
                Learner(name="Asha", city="Pune"),
                Learner(name="Rohan", city="Mumbai"),
                Learner(name="Mira", city="Pune"),
            ]
        )
        session.commit()

        rows = session.exec(select(Learner).where(Learner.city == "Pune")).all()
        for row in rows:
            print(row.name, row.city)


if __name__ == "__main__":
    main()
