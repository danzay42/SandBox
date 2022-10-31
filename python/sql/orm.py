from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import DateTime, Integer, String

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "Customer"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))

    def __repr__(self) -> str:
        return (
            f"Customer(id={self.id!r})",
            f"first_name={self.first_name!r}",
            f"last_name={self.last_name!r}"
        ) 


class Invoice(Base):
    __tablename__ = "Invoice"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    total: Mapped[int] = mapped_column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Invoice(id={self.id!r})",
            f"customer_id={self.customer_id!r}",
            f"date={self.date!r}"
        )


number_of_customers = int(
    input("How many customers do you want to query? ")
)
db_path = Path("sample.db").absolute()
engine = create_engine(rf"sqlite:///{db_path}")
session = Session(engine)
stmt = (
    select(
        Customer.id,
        Customer.first_name,
        func.sum(Invoice.total).label("Total"),
    )
    .join(Invoice, Customer.id == Invoice.customer_id)
    .group_by(Customer.id, Customer.first_name)
    .order_by(func.sum(Invoice.total).label("Total").desc())
    .limit(number_of_customers)
)

for customer in session.execute(stmt):
    print(customer)
