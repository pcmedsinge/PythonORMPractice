import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)
engine = create_engine(DB_URL)


class Item(SQLModel, table=True):
    __tablename__ = "sm_api_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float


app = FastAPI(title="SQLModel Lab API")


@app.on_event("startup")
def startup() -> None:
    SQLModel.metadata.create_all(engine, tables=[Item.__table__])


@app.post("/items", response_model=Item)
def create_item(item: Item) -> Item:
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/items", response_model=list[Item])
def list_items(min_price: float | None = None) -> list[Item]:
    with Session(engine) as session:
        query = select(Item)
        if min_price is not None:
            query = query.where(Item.price >= min_price)
        return session.exec(query.order_by(Item.id)).all()


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
