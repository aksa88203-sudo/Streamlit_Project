from datetime import date

from sqlalchemy import Select, extract, func, select
from sqlalchemy.orm import Session

from app.models.sale import Sale


class SaleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, skip: int = 0, limit: int = 200, year: int | None = None, month: int | None = None) -> list[Sale]:
        stmt: Select[tuple[Sale]] = select(Sale)
        if year:
            stmt = stmt.where(extract("year", Sale.sale_date) == year)
        if month:
            stmt = stmt.where(extract("month", Sale.sale_date) == month)
        stmt = stmt.offset(skip).limit(limit).order_by(Sale.sale_date.desc(), Sale.id.desc())
        return list(self.db.scalars(stmt))

    def create(self, sale: Sale) -> Sale:
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def sum_for_day(self, day: date) -> float:
        value = self.db.scalar(select(func.coalesce(func.sum(Sale.total), 0)).where(Sale.sale_date == day))
        return float(value or 0)

    def count_for_day(self, day: date) -> int:
        value = self.db.scalar(select(func.count()).select_from(Sale).where(Sale.sale_date == day))
        return int(value or 0)

    def month_rows(self, year: int, month: int) -> list[Sale]:
        stmt: Select[tuple[Sale]] = (
            select(Sale)
            .where(extract("year", Sale.sale_date) == year)
            .where(extract("month", Sale.sale_date) == month)
            .order_by(Sale.sale_date.asc(), Sale.id.asc())
        )
        return list(self.db.scalars(stmt))

    def product_sales_totals(self) -> list[tuple[str, int]]:
        stmt = select(Sale.product_name, func.coalesce(func.sum(Sale.quantity), 0)).group_by(Sale.product_name)
        return [(row[0], int(row[1])) for row in self.db.execute(stmt).all()]
