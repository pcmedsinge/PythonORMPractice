import os
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Client(SQLModel, table=True):
    __tablename__ = "sm_clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Invoice(SQLModel, table=True):
    __tablename__ = "sm_invoices"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="sm_clients.id")
    amount: float


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        c1 = Client(name="Acme Retail")
        c2 = Client(name="North Mart")
        session.add_all([c1, c2])
        session.commit()
        session.refresh(c1)
        session.refresh(c2)

        session.add_all(
            [
                Invoice(client_id=c1.id, amount=1400),
                Invoice(client_id=c1.id, amount=600),
                Invoice(client_id=c2.id, amount=1200),
            ]
        )
        session.commit()

        report = session.exec(
            select(Client.name, func.sum(Invoice.amount))
            .join(Invoice, Client.id == Invoice.client_id)
            .group_by(Client.name)
            .order_by(Client.name)
        ).all()

        for name, total in report:
            print(name, float(total))


if __name__ == "__main__":
    main()
