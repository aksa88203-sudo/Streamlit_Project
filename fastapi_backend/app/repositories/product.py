from __future__ import annotations

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> list[Product]:
        stmt: Select[tuple[Product]] = select(Product).offset(skip).limit(limit).order_by(Product.id.desc())
        return list(self.db.scalars(stmt))

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        stmt: Select[tuple[Product]] = select(Product).where(Product.sku == sku)
        return self.db.scalar(stmt)

    def get_by_name(self, name: str) -> Product | None:
        stmt: Select[tuple[Product]] = select(Product).where(Product.name == name)
        return self.db.scalar(stmt)

    def create(self, payload: ProductCreate) -> Product:
        db_product = Product(**payload.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update(self, db_product: Product, payload: ProductUpdate) -> Product:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_product, field, value)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def save(self, db_product: Product) -> Product:
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, db_product: Product) -> None:
        self.db.delete(db_product)
        self.db.commit()

    def count_total(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Product)) or 0)

    def count_low_stock(self) -> int:
        return int(
            self.db.scalar(select(func.count()).select_from(Product).where(Product.quantity <= Product.reorder_level))
            or 0
        )

    def count_overstocked(self) -> int:
        return int(
            self.db.scalar(select(func.count()).select_from(Product).where(Product.quantity > Product.max_stock)) or 0
        )

    def list_low_stock(self) -> list[Product]:
        stmt: Select[tuple[Product]] = select(Product).where(Product.quantity <= Product.reorder_level).order_by(Product.id.desc())
        return list(self.db.scalars(stmt))

    def list_overstocked(self) -> list[Product]:
        stmt: Select[tuple[Product]] = select(Product).where(Product.quantity > Product.max_stock).order_by(Product.id.desc())
        return list(self.db.scalars(stmt))
