from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Sale(Base, TimestampMixin):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True, index=True)
    product_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
