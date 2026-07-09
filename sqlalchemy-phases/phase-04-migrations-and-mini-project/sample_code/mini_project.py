import os
from sqlalchemy import String, Integer, ForeignKey, Numeric, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "sa_customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")


class Order(Base):
    __tablename__ = "sa_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("sa_customers.id"))
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    customer: Mapped[Customer] = relationship(back_populates="orders")


def main() -> None:
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine, tables=[Order.__table__, Customer.__table__])
    Base.metadata.create_all(engine, tables=[Customer.__table__, Order.__table__])

    with Session(engine) as session:
        c1 = Customer(name="Acme Retail")
        c2 = Customer(name="North Mart")
        session.add_all([c1, c2])
        session.flush()

        session.add_all(
            [
                Order(customer_id=c1.id, total_amount=1400),
                Order(customer_id=c1.id, total_amount=600),
                Order(customer_id=c2.id, total_amount=1200),
            ]
        )
        session.commit()

        report = session.execute(
            select(Customer.name, func.sum(Order.total_amount))
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.name)
            .order_by(Customer.name)
        ).all()

        for name, total in report:
            print(name, float(total))


if __name__ == "__main__":
    main()
