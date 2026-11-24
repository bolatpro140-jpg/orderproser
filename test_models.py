from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models import RefundRequest


def test_valid_refund_request():
    request = RefundRequest(
        order_id=1, reason="Товар пришёл повреждённым", refund_amount=Decimal("49.90")
    )
    assert request.refund_amount == Decimal("49.90")


def test_short_reason_rejected():
    with pytest.raises(ValidationError) as exc:
        RefundRequest(order_id=1, reason="мало", refund_amount=Decimal(10))
    assert "reason" in str(exc.value)


@pytest.mark.parametrize("amount", [Decimal(-5), Decimal(0)])
def test_non_positive_amount_rejected(amount):
    with pytest.raises(ValidationError):
        RefundRequest(order_id=1, reason="Не подошёл размер", refund_amount=amount)
