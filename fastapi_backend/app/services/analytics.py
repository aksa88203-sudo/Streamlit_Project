from datetime import date

from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.sale import SaleRepository


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.product_repo = ProductRepository(db)
        self.sale_repo = SaleRepository(db)

    def get_dashboard_summary(self):
        today = date.today()
        return {
            "total_products": self.product_repo.count_total(),
            "low_stock": self.product_repo.count_low_stock(),
            "overstocked": self.product_repo.count_overstocked(),
            "today_sales_amount": round(self.sale_repo.sum_for_day(today), 2),
            "today_sales_count": self.sale_repo.count_for_day(today),
        }

    def get_monthly_report(self, year: int, month: int):
        sales = self.sale_repo.month_rows(year=year, month=month)
        total_revenue = round(sum(float(s.total) for s in sales), 2)
        total_items = sum(int(s.quantity) for s in sales)
        avg_sale = round((total_revenue / len(sales)) if sales else 0, 2)

        daily_map: dict[str, float] = {}
        product_map: dict[str, int] = {}
        for s in sales:
            key = s.sale_date.isoformat()
            daily_map[key] = round(daily_map.get(key, 0) + float(s.total), 2)
            product_map[s.product_name] = product_map.get(s.product_name, 0) + int(s.quantity)

        daily_revenue = [{"date": key, "revenue": value} for key, value in sorted(daily_map.items())]
        top_products = [
            {"product": name, "quantity": qty}
            for name, qty in sorted(product_map.items(), key=lambda item: item[1], reverse=True)
        ]

        return {
            "year": year,
            "month": month,
            "total_revenue": total_revenue,
            "total_items_sold": total_items,
            "avg_sale_value": avg_sale,
            "daily_revenue": daily_revenue,
            "top_products": top_products,
        }

    def get_alerts(self):
        low_stock = []
        overstocked = []
        predictions = []

        for p in self.product_repo.list_low_stock():
            low_stock.append(
                {
                    "alert_type": "low_stock",
                    "product": p.name,
                    "sku": p.sku,
                    "quantity": int(p.quantity),
                    "message": f"Restock needed - {int(p.reorder_level) - int(p.quantity)} units below threshold",
                }
            )

        for p in self.product_repo.list_overstocked():
            overstocked.append(
                {
                    "alert_type": "overstocked",
                    "product": p.name,
                    "sku": p.sku,
                    "quantity": int(p.quantity),
                    "message": f"Overstocked by {int(p.quantity) - int(p.max_stock)} units",
                }
            )

        sales_totals = dict(self.sale_repo.product_sales_totals())
        for p in self.product_repo.list(skip=0, limit=5000):
            avg_daily = sales_totals.get(p.name, 0) / 365.0
            if avg_daily <= 0:
                continue
            days_until_reorder = (int(p.quantity) - int(p.reorder_level)) / avg_daily
            if 0 < days_until_reorder < 7:
                predictions.append(
                    {"product": p.name, "message": f"At current sales rate, reorder in ~{int(days_until_reorder)} days"}
                )
            elif days_until_reorder <= 0:
                predictions.append({"product": p.name, "message": "Already below reorder level"})

        return {"low_stock": low_stock, "overstocked": overstocked, "predictions": predictions}
