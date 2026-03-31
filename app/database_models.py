from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Wallet(Base):
    __tablename__ = "wallet"


    id: Mapped[int] = mapped_column(primary_key=True)  # primary_key - признак, который объясняет БД, что этот атрибут является уникальным.
    name: Mapped[str]
    balance: Mapped[Decimal]  # не может быть float, т.к. в python проблема с округлением.

