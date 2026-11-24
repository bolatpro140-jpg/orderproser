"""Эталонная модель заказа на Pydantic v2 для проекта order-processor-lab."""

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderStatus(StrEnum):
    NEW = "new"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    sku: str = Field(min_length=3, max_length=32, description="Артикул товара")
    quantity: int = Field(gt=0, le=1000, description="Количество единиц")
    unit_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class Order(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    order_id: int = Field(gt=0, description="Идентификатор заказа")
    customer_email: str = Field(min_length=5, max_length=254)
    items: list[OrderItem] = Field(min_length=1)
    status: OrderStatus = OrderStatus.NEW
    comment: str | None = Field(default=None, max_length=500)

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError(
                "Некорректный email: ожидается формат name@domain"
            )
        return value.lower()

    @field_validator("items")
    @classmethod
    def validate_unique_skus(cls, value: list[OrderItem]) -> list[OrderItem]:
        skus = [item.sku for item in value]
        if len(skus) != len(set(skus)):
            raise ValueError("Артикулы товаров в заказе не должны повторяться")
        return value

    @property
    def total(self) -> Decimal:
        return sum(
            (item.unit_price * item.quantity for item in self.items), Decimal(0)
        )
