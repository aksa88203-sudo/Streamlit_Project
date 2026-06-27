from fastapi import APIRouter

from app.api.v1.endpoints import ai, analytics, auth, items, products, sales

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(sales.router)
api_router.include_router(analytics.router)
api_router.include_router(ai.router)
