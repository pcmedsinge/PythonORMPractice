import os
from sqlalchemy import String, Integer, Numeric, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Sale(Base):
    __tablename__ = "sa_sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))


def main() -> None:
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine, tables=[Sale.__table__])
    Base.metadata.create_all(engine, tables=[Sale.__table__])

    with Session(engine) as session:
        session.add_all(
            [
                Sale(region="West", amount=1200),
                Sale(region="West", amount=900),
                Sale(region="East", amount=1500),
                Sale(region="East", amount=700),
            ]
        )
        session.commit()

        report = session.execute(
            select(Sale.region, func.sum(Sale.amount).label("total"))
            .group_by(Sale.region)
            .order_by(Sale.region)
        ).all()

        for region, total in report:
            print(region, float(total))


if __name__ == "__main__":
    main()
