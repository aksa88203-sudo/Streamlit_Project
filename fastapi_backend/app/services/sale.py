from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.repositories.product import ProductRepository
from app.repositories.sale import SaleRepository
from app.schemas.sale import SaleCreate


class SaleService:
    def __init__(self, db: Session) -> None:
        self.product_repo = ProductRepository(db)
        self.sale_repo = SaleRepository(db)

    def list_sales(self, skip: int = 0, limit: int = 200, year: int | None = None, month: int | None = None):
        return self.sale_repo.list(skip=skip, limit=limit, year=year, month=month)

    def create_sale(self, payload: SaleCreate):
        product = None
        if payload.product_id is not None:
            product = self.product_repo.get_by_id(payload.product_id)
        elif payload.product_name:
            product = self.product_repo.get_by_name(payload.product_name)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Frontend behavior: quantity does not go below zero.
        product.quantity = max(0, int(product.quantity) - payload.quantity)
        self.product_repo.save(product)

        sale = Sale(
            sale_date=payload.sale_date or date.today(),
            product_id=product.id,
            product_name=product.name,
            quantity=payload.quantity,
            total=round(float(product.price) * payload.quantity, 2),
        )
        return self.sale_repo.create(sale)
