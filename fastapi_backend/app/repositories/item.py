from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> list[Item]:
        stmt: Select[tuple[Item]] = select(Item).offset(skip).limit(limit).order_by(Item.id.desc())
        return list(self.db.scalars(stmt))

    def get_by_id(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def get_by_sku(self, sku: str) -> Item | None:
        stmt: Select[tuple[Item]] = select(Item).where(Item.sku == sku)
        return self.db.scalar(stmt)

    def create(self, payload: ItemCreate) -> Item:
        db_item = Item(**payload.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, db_item: Item, payload: ItemUpdate) -> Item:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, db_item: Item) -> None:
        self.db.delete(db_item)
        self.db.commit()
