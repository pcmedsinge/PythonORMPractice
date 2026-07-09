import os
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Supplier(SQLModel, table=True):
    __tablename__ = "sm_cap_suppliers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    __tablename__ = "sm_cap_products"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    unit_price: float


class PurchaseOrder(SQLModel, table=True):
    __tablename__ = "sm_cap_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_id: int = Field(foreign_key="sm_cap_suppliers.id")


class PurchaseOrderItem(SQLModel, table=True):
    __tablename__ = "sm_cap_order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="sm_cap_orders.id")
    product_id: int = Field(foreign_key="sm_cap_products.id")
    quantity: int


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        s1 = Supplier(name="Delta Supplies")
        s2 = Supplier(name="Bluebell Traders")
        p1 = Product(title="Fluent SQL", unit_price=500)
        p2 = Product(title="Python at Scale", unit_price=700)
        p3 = Product(title="Django Patterns", unit_price=650)
        session.add_all([s1, s2, p1, p2, p3])
        session.commit()
        session.refresh(s1)
        session.refresh(s2)
        session.refresh(p1)
        session.refresh(p2)
        session.refresh(p3)

        o1 = PurchaseOrder(supplier_id=s1.id)
        o2 = PurchaseOrder(supplier_id=s2.id)
        session.add_all([o1, o2])
        session.commit()
        session.refresh(o1)
        session.refresh(o2)

        session.add_all(
            [
                PurchaseOrderItem(order_id=o1.id, product_id=p1.id, quantity=3),
                PurchaseOrderItem(order_id=o1.id, product_id=p2.id, quantity=2),
                PurchaseOrderItem(order_id=o2.id, product_id=p2.id, quantity=4),
                PurchaseOrderItem(order_id=o2.id, product_id=p3.id, quantity=5),
            ]
        )
        session.commit()

        top_products = session.exec(
            select(Product.title, func.sum(PurchaseOrderItem.quantity).label("qty"))
            .join(PurchaseOrderItem, Product.id == PurchaseOrderItem.product_id)
            .group_by(Product.title)
            .order_by(func.sum(PurchaseOrderItem.quantity).desc())
            .limit(3)
        ).all()

        print("Top products:")
        for title, qty in top_products:
            print(title, int(qty))

        supplier_total = session.exec(
            select(
                Supplier.name,
                func.sum(PurchaseOrderItem.quantity * Product.unit_price).label("total"),
            )
            .join(PurchaseOrder, Supplier.id == PurchaseOrder.supplier_id)
            .join(PurchaseOrderItem, PurchaseOrder.id == PurchaseOrderItem.order_id)
            .join(Product, Product.id == PurchaseOrderItem.product_id)
            .group_by(Supplier.name)
            .order_by(func.sum(PurchaseOrderItem.quantity * Product.unit_price).desc())
        ).all()

        print("Total by supplier:")
        for name, total in supplier_total:
            print(name, float(total))

        print("Migration note: add tax_percent NUMERIC(5,2) NOT NULL DEFAULT 0 to sm_cap_orders")


if __name__ == "__main__":
    main()
