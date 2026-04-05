from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)  # unique атрибут уникальности




# имя кошелька в БД
class Wallet(Base):
    # название таблицы
    __tablename__ = "wallet"


    id: Mapped[int] = mapped_column(primary_key=True)  # primary_key - признак, который объясняет БД, что этот атрибут является уникальным.
    name: Mapped[str]
    balance: Mapped[Decimal]  # Не может быть float, тк в python проблема с округлением.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # ForeignKey("user.id") ссылаемся кошельком на конкретного юзера.
    # Получается связь 1 ко многим (у юзера user_id может быть много wallet, но у wallet может быть только 1 user_id)
    # nullable=False - кошелек не может быть создан без юзера
