from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SaleCreate(BaseModel):
    product_id: int | None = None
    product_name: str | None = Field(default=None, min_length=2, max_length=120)
    quantity: int = Field(ge=1)
    sale_date: date | None = None

    @model_validator(mode="after")
    def validate_product_reference(self):
        if self.product_id is None and not self.product_name:
            raise ValueError("Either product_id or product_name is required")
        return self


class SaleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale_date: date
    product_id: int | None
    product_name: str
    quantity: int
    total: float
    created_at: datetime
    updated_at: datetime
