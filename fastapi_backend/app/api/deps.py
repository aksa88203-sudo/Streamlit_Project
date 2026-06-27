from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analytics import AnalyticsService
from app.services.ai_suite import AISuiteService
from app.services.auth import AuthService
from app.services.item import ItemService
from app.services.product import ProductService
from app.services.sale import SaleService


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    return SaleService(db)


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(db)


def get_ai_suite_service(db: Session = Depends(get_db)) -> AISuiteService:
    return AISuiteService(db)
