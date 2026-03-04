from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: Session) -> None:
        self.repo = ItemRepository(db)

    def list_items(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)

    def get_item(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item

    def create_item(self, payload: ItemCreate):
        existing = self.repo.get_by_sku(payload.sku)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SKU already exists")
        return self.repo.create(payload)

    def update_item(self, item_id: int, payload: ItemUpdate):
        db_item = self.get_item(item_id)
        return self.repo.update(db_item, payload)

    def delete_item(self, item_id: int):
        db_item = self.get_item(item_id)
        self.repo.delete(db_item)
