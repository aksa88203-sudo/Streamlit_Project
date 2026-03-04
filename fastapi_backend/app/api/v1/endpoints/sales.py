from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_sale_service
from app.schemas.sale import SaleCreate, SaleRead
from app.services.sale import SaleService

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=list[SaleRead])
def list_sales(
    skip: int = 0,
    limit: int = 300,
    year: int | None = Query(default=None, ge=2020),
    month: int | None = Query(default=None, ge=1, le=12),
    service: SaleService = Depends(get_sale_service),
):
    return service.list_sales(skip=skip, limit=limit, year=year, month=month)


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(payload: SaleCreate, service: SaleService = Depends(get_sale_service)):
    return service.create_sale(payload)
