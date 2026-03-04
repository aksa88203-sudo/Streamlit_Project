from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_item_service
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item import ItemService

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemRead])
def list_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service),
):
    return service.list_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    return service.get_item(item_id)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(payload)


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, service: ItemService = Depends(get_item_service)):
    return service.update_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    service.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
