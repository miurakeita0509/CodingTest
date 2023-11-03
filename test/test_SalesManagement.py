import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.SalesManagement import SalesManagement


@pytest.mark.parametrize(
    (
        "juice_price",
        "expected_result",
    ),
    [
        (120, True),
    ],
)
def test_record_juice_sales_normal(juice_price, expected_result):
    sales_management = SalesManagement()
    result = sales_management.record_juice_sales(juice_price)

    assert sales_management.get_sales() == 120
    assert result == expected_result
