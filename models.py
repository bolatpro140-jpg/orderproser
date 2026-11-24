"""Модели запросов order-processor-lab."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RefundRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    order_id: int = Field(gt=0, description="Идентификатор заказа")
    reason: str = Field(min_length=10, max_length=500, description="Причина возврата")
    refund_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, value: str) -> str:
        if len(value) < 10:
            raise ValueError("Причина возврата должна содержать минимум 10 символов")
        return value
