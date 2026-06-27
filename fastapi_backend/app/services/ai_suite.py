from __future__ import annotations

from datetime import date

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.product import ProductRepository
from app.repositories.sale import SaleRepository


class AISuiteService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.settings = get_settings()
        self.product_repo = ProductRepository(db)
        self.sale_repo = SaleRepository(db)

    def generate_insight(self, focus: str, question: str | None = None) -> dict[str, str]:
        context = self._build_context()
        fallback = self._fallback_response(context=context, focus=focus, question=question)

        api_key = self.settings.GEMINI_API_KEY
        model = self.settings.GEMINI_MODEL
        if not api_key:
            return {
                "focus": focus,
                "model": "local-fallback",
                "source": "fallback",
                "content": fallback,
            }

        prompt = self._build_prompt(context=context, focus=focus, question=question)
        try:
            response = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                headers={
                    "x-goog-api-key": api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "system_instruction": {
                        "parts": [
                            {
                                "text": (
                                    "You are an inventory operations AI assistant. "
                                    "Give concise, practical markdown advice for a small inventory business. "
                                    "Use short sections and action-oriented recommendations."
                                )
                            }
                        ]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": prompt,
                                }
                            ],
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.4,
                    },
                },
                timeout=20.0,
            )
            response.raise_for_status()
            data = response.json()
            text = self._extract_text(data)
            if not text:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="AI service returned an empty response",
                )
            return {
                "focus": focus,
                "model": model,
                "source": "gemini",
                "content": text,
            }
        except Exception:
            return {
                "focus": focus,
                "model": "local-fallback",
                "source": "fallback",
                "content": fallback,
            }

    def _build_context(self) -> dict[str, object]:
        products = self.product_repo.list(skip=0, limit=5000)
        sales = self.sale_repo.list(skip=0, limit=500)
        today = date.today().isoformat()

        total_stock_units = sum(int(p.quantity) for p in products)
        inventory_value = round(sum(float(p.price) * int(p.quantity) for p in products), 2)

        category_totals: dict[str, int] = {}
        for product in products:
            category = product.category or "Other"
            category_totals[category] = category_totals.get(category, 0) + int(product.quantity)

        top_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)[:5]

        top_sellers_map: dict[str, int] = {}
        for sale in sales:
            top_sellers_map[sale.product_name] = top_sellers_map.get(sale.product_name, 0) + int(sale.quantity)
        top_sellers = sorted(top_sellers_map.items(), key=lambda item: item[1], reverse=True)[:5]

        recent_sales = [
            {
                "date": sale.sale_date.isoformat(),
                "product": sale.product_name,
                "quantity": int(sale.quantity),
                "total": round(float(sale.total), 2),
            }
            for sale in sales[:10]
        ]

        low_stock = [
            {
                "name": product.name,
                "sku": product.sku,
                "quantity": int(product.quantity),
                "reorder_level": int(product.reorder_level),
            }
            for product in self.product_repo.list_low_stock()[:8]
        ]
        overstocked = [
            {
                "name": product.name,
                "sku": product.sku,
                "quantity": int(product.quantity),
                "max_stock": int(product.max_stock),
            }
            for product in self.product_repo.list_overstocked()[:8]
        ]

        return {
            "today": today,
            "total_products": len(products),
            "total_stock_units": total_stock_units,
            "inventory_value": inventory_value,
            "low_stock_count": len(low_stock),
            "overstocked_count": len(overstocked),
            "sales_count": len(sales),
            "top_categories": top_categories,
            "top_sellers": top_sellers,
            "recent_sales": recent_sales,
            "low_stock": low_stock,
            "overstocked": overstocked,
        }

    def _build_prompt(self, context: dict[str, object], focus: str, question: str | None) -> str:
        prompt_parts = [
            f"Date: {context['today']}",
            "Inventory snapshot:",
            f"- Total products: {context['total_products']}",
            f"- Total stock units: {context['total_stock_units']}",
            f"- Inventory value: ${context['inventory_value']}",
            f"- Low stock count: {context['low_stock_count']}",
            f"- Overstocked count: {context['overstocked_count']}",
            f"- Sales records available: {context['sales_count']}",
            f"- Top categories by units: {context['top_categories']}",
            f"- Top sellers: {context['top_sellers']}",
            f"- Low stock products: {context['low_stock']}",
            f"- Overstocked products: {context['overstocked']}",
            f"- Recent sales: {context['recent_sales']}",
        ]

        if focus == "overview":
            prompt_parts.append(
                "Give an executive inventory overview with strengths, risks, and the top 3 recommended actions."
            )
        elif focus == "reorder":
            prompt_parts.append(
                "Focus on reorder planning. Highlight urgent restocks, slow-moving inventory, and what to buy next."
            )
        elif focus == "sales":
            prompt_parts.append(
                "Focus on sales patterns. Explain top-selling items, recent sales momentum, and merchandising ideas."
            )
        else:
            prompt_parts.append(f"User question: {question or 'Provide practical inventory guidance.'}")

        prompt_parts.append("Respond in concise markdown.")
        return "\n".join(prompt_parts)

    def _fallback_response(self, context: dict[str, object], focus: str, question: str | None) -> str:
        top_sellers = context["top_sellers"]
        low_stock = context["low_stock"]
        overstocked = context["overstocked"]

        lines = [
            "## AI Suite",
            f"- Focus: {focus.title()}",
            f"- Total products: {context['total_products']}",
            f"- Inventory value: ${context['inventory_value']}",
            f"- Low stock items: {context['low_stock_count']}",
            f"- Overstocked items: {context['overstocked_count']}",
        ]

        if top_sellers:
            lines.append("")
            lines.append("### Top Sellers")
            for name, qty in top_sellers[:3]:
                lines.append(f"- {name}: {qty} units sold")

        if low_stock:
            lines.append("")
            lines.append("### Reorder Priority")
            for item in low_stock[:3]:
                gap = int(item["reorder_level"]) - int(item["quantity"])
                lines.append(f"- {item['name']} is {gap} units below reorder level")

        if overstocked:
            lines.append("")
            lines.append("### Overstock Watch")
            for item in overstocked[:3]:
                excess = int(item["quantity"]) - int(item["max_stock"])
                lines.append(f"- {item['name']} is overstocked by {excess} units")

        if question:
            lines.append("")
            lines.append("### Your Question")
            lines.append(f"- {question}")

        lines.append("")
        lines.append("### Suggested Actions")
        lines.append("- Restock the most urgent low-stock products first.")
        lines.append("- Push promotions or bundles for overstocked products.")
        lines.append("- Review recent top sellers before placing the next purchase order.")
        return "\n".join(lines)

    @staticmethod
    def _extract_text(data: dict[str, object]) -> str:
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        first = candidates[0] if isinstance(candidates, list) else {}
        content = first.get("content", {}) if isinstance(first, dict) else {}
        parts = content.get("parts", []) if isinstance(content, dict) else []
        texts: list[str] = []
        for part in parts:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                texts.append(part["text"])
        return "\n".join(texts).strip()
