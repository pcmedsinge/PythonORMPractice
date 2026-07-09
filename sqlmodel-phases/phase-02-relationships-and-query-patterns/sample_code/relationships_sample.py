import os
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select

DB_URL = os.getenv(
    "SQLMODEL_DATABASE_URL",
    "postgresql+psycopg://orm_user:orm_pass@localhost:55432/orm_sqlmodel",
)


class Team(SQLModel, table=True):
    __tablename__ = "sm_teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    members: List["Member"] = Relationship(back_populates="team")


class Member(SQLModel, table=True):
    __tablename__ = "sm_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: int = Field(foreign_key="sm_teams.id")
    team: Optional[Team] = Relationship(back_populates="members")


def main() -> None:
    engine = create_engine(DB_URL)
    SQLModel.metadata.drop_all(engine, tables=[Member.__table__, Team.__table__])
    SQLModel.metadata.create_all(engine, tables=[Team.__table__, Member.__table__])

    with Session(engine) as session:
        t1 = Team(name="Platform")
        t2 = Team(name="Data")
        session.add_all([t1, t2])
        session.commit()
        session.refresh(t1)
        session.refresh(t2)

        session.add_all(
            [
                Member(name="Ira", team_id=t1.id),
                Member(name="Manav", team_id=t1.id),
                Member(name="Sara", team_id=t2.id),
            ]
        )
        session.commit()

        rows = session.exec(select(Member).where(Member.team_id == t1.id)).all()
        print("Platform members:", [r.name for r in rows])


if __name__ == "__main__":
    main()
