from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_products: int
    low_stock: int
    overstocked: int
    today_sales_amount: float
    today_sales_count: int


class DailyRevenue(BaseModel):
    date: str
    revenue: float


class TopProduct(BaseModel):
    product: str
    quantity: int


class MonthlyReport(BaseModel):
    year: int
    month: int
    total_revenue: float
    total_items_sold: int
    avg_sale_value: float
    daily_revenue: list[DailyRevenue]
    top_products: list[TopProduct]


class InventoryAlert(BaseModel):
    alert_type: str
    product: str
    sku: str
    quantity: int
    message: str


class PredictionAlert(BaseModel):
    product: str
    message: str


class AlertsResponse(BaseModel):
    low_stock: list[InventoryAlert]
    overstocked: list[InventoryAlert]
    predictions: list[PredictionAlert]
