import os
from typing import Optional, Iterator
from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)
engine = create_engine(DB_URL)


class Product(SQLModel, table=True):
    __tablename__ = "sm_api_products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


app = FastAPI(title="SQLModel Practice API")


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine, tables=[Product.__table__])


@app.post("/products", response_model=Product)
def create_product(payload: Product) -> Product:
    with Session(engine) as session:
        session.add(payload)
        session.commit()
        session.refresh(payload)
        return payload


@app.get("/products", response_model=list[Product])
def list_products() -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product).order_by(Product.id)).all()
