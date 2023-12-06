from typing import Optional

from sqlalchemy import Integer, ForeignKey, BIGINT, String, DECIMAL, Boolean, false, JSON
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, TimestampMixin


class UserContracts(Base, TimestampMixin):
    __tablename__ = "user_contracts"
    contract_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    contract_name: Mapped[str] = mapped_column(String(100))
    contract_address: Mapped[str] = mapped_column(String(100))
    contract_description: Mapped[str] = mapped_column(String(100))


