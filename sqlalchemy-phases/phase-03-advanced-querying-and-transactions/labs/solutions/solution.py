import os
from sqlalchemy import String, Integer, Numeric, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Revenue(Base):
    __tablename__ = "sa_revenue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))


class Wallet(Base):
    __tablename__ = "sa_wallet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(50), unique=True)
    balance: Mapped[float] = mapped_column(Numeric(10, 2))


def transfer_credits(session: Session, from_owner: str, to_owner: str, amount: float) -> None:
    source = session.scalar(select(Wallet).where(Wallet.owner == from_owner))
    target = session.scalar(select(Wallet).where(Wallet.owner == to_owner))
    if not source or not target:
        raise ValueError("Wallet not found")
    if float(source.balance) < amount:
        raise ValueError("Insufficient balance")
    source.balance = float(source.balance) - amount
    target.balance = float(target.balance) + amount


def main() -> None:
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine, tables=[Revenue.__table__, Wallet.__table__])
    Base.metadata.create_all(engine, tables=[Revenue.__table__, Wallet.__table__])

    with Session(engine) as session:
        session.add_all(
            [
                Revenue(category="books", amount=400),
                Revenue(category="books", amount=700),
                Revenue(category="courses", amount=1200),
                Revenue(category="courses", amount=800),
                Revenue(category="tools", amount=300),
            ]
        )
        session.add_all(
            [
                Wallet(owner="Rita", balance=500),
                Wallet(owner="Sahil", balance=100),
            ]
        )
        session.commit()

        report = session.execute(
            select(
                Revenue.category,
                func.sum(Revenue.amount).label("total_revenue"),
                func.avg(Revenue.amount).label("avg_revenue"),
            )
            .group_by(Revenue.category)
            .order_by(func.sum(Revenue.amount).desc())
        ).all()

        print("Revenue report:")
        for category, total, avg in report:
            print(category, float(total), round(float(avg), 2))

        try:
            transfer_credits(session, "Rita", "Sahil", 120)
            session.commit()
            print("Transfer 1 success")
        except Exception as ex:
            session.rollback()
            print("Transfer 1 failed:", ex)

        try:
            transfer_credits(session, "Sahil", "Rita", 1000)
            session.commit()
            print("Transfer 2 success")
        except Exception as ex:
            session.rollback()
            print("Transfer 2 failed:", ex)

        balances = session.scalars(select(Wallet).order_by(Wallet.owner)).all()
        print("Final balances:")
        for row in balances:
            print(row.owner, float(row.balance))


if __name__ == "__main__":
    main()
