import os
from sqlalchemy import String, Integer, ForeignKey, Numeric, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlalchemy",
)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "sa_cap_customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Book(Base):
    __tablename__ = "sa_cap_books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)


class BookOrder(Base):
    __tablename__ = "sa_cap_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("sa_cap_customers.id"))


class BookOrderItem(Base):
    __tablename__ = "sa_cap_order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("sa_cap_orders.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("sa_cap_books.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)


def main() -> None:
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        c1 = Customer(name="Delta Library")
        c2 = Customer(name="Bluebell School")
        b1 = Book(title="Fluent SQL", unit_price=500)
        b2 = Book(title="Python at Scale", unit_price=700)
        b3 = Book(title="Django Patterns", unit_price=650)
        session.add_all([c1, c2, b1, b2, b3])
        session.flush()

        o1 = BookOrder(customer_id=c1.id)
        o2 = BookOrder(customer_id=c2.id)
        session.add_all([o1, o2])
        session.flush()

        session.add_all(
            [
                BookOrderItem(order_id=o1.id, book_id=b1.id, quantity=3),
                BookOrderItem(order_id=o1.id, book_id=b2.id, quantity=2),
                BookOrderItem(order_id=o2.id, book_id=b2.id, quantity=4),
                BookOrderItem(order_id=o2.id, book_id=b3.id, quantity=5),
            ]
        )
        session.commit()

        top_books = session.execute(
            select(Book.title, func.sum(BookOrderItem.quantity).label("qty"))
            .join(BookOrderItem, Book.id == BookOrderItem.book_id)
            .group_by(Book.title)
            .order_by(func.sum(BookOrderItem.quantity).desc())
            .limit(3)
        ).all()

        print("Top books by quantity:")
        for title, qty in top_books:
            print(title, int(qty))

        customer_spend = session.execute(
            select(
                Customer.name,
                func.sum(BookOrderItem.quantity * Book.unit_price).label("total_spend"),
            )
            .join(BookOrder, Customer.id == BookOrder.customer_id)
            .join(BookOrderItem, BookOrder.id == BookOrderItem.order_id)
            .join(Book, Book.id == BookOrderItem.book_id)
            .group_by(Customer.name)
            .order_by(func.sum(BookOrderItem.quantity * Book.unit_price).desc())
        ).all()

        print("Total spend by customer:")
        for name, total in customer_spend:
            print(name, float(total))

        print("Migration note: add discount_percent NUMERIC(5,2) NOT NULL DEFAULT 0 to sa_cap_orders")


if __name__ == "__main__":
    main()
