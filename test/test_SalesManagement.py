import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.SalesManagement import SalesManagement


class MockJuiceManagement:
    def __init__(self):
        self.juice = {
            "コーラ": {"name": "コーラ", "price": 120, "stock": 5},
        }

    def get_juice_info(self, juice_name=None):
        if juice_name:
            return self.juice.get(juice_name)
        return self.juice


@pytest.mark.parametrize(
    (
        "juice_name",
        "expected_sales",
        "expected_result",
    ),
    [
        ("コーラ", 120, True),
    ],
)
def test_DataStore_normal(juice_name, expected_sales, expected_result):
    juice_management = MockJuiceManagement()
    data_store = SalesManagement()
    result = data_store.record_juice_sales(juice_management, juice_name)

    assert data_store.get_sales() == expected_sales
    assert result == expected_result
