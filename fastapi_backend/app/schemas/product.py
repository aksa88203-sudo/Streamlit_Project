from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    sku: str = Field(min_length=2, max_length=64)
    quantity: int = Field(ge=0, default=0)
    reorder_level: int = Field(ge=0, default=0)
    max_stock: int = Field(ge=1, default=100)
    price: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=80, default="Other")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    quantity: int | None = Field(default=None, ge=0)
    reorder_level: int | None = Field(default=None, ge=0)
    max_stock: int | None = Field(default=None, ge=1)
    price: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=80)


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
