from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_product_service
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductRead])
def list_products(skip: int = 0, limit: int = 200, service: ProductService = Depends(get_product_service)):
    return service.list_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    return service.get_product(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create_product(payload)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, service: ProductService = Depends(get_product_service)):
    return service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
