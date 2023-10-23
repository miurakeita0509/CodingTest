import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.JuiceManagement import JuiceManagement


def test_init_normal():
    jm = JuiceManagement()
    expected_juices = {
        "cola": {"name": "コーラ", "price": 120, "stock": 5},
    }
    assert jm.get_juice_info() == expected_juices


@pytest.mark.parametrize(
    ("juice", "expected_value"),
    [
        ("cola", {"name": "コーラ", "price": 120, "stock": 5}),
        ("test", None),
    ],
)
def test_get_juice_info(juice, expected_value):
    jm = JuiceManagement()
    assert jm.get_juice_info(juice) == expected_value
