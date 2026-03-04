from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def list_products(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)

    def get_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    def create_product(self, payload: ProductCreate):
        existing = self.repo.get_by_sku(payload.sku)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SKU already exists")
        return self.repo.create(payload)

    def update_product(self, product_id: int, payload: ProductUpdate):
        db_product = self.get_product(product_id)
        return self.repo.update(db_product, payload)

    def delete_product(self, product_id: int):
        db_product = self.get_product(product_id)
        self.repo.delete(db_product)
