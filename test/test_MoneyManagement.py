import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.MoneyManagement import MoneyManagement


@pytest.mark.parametrize(
    ("input_str", "expected_value"),
    [
        ("10", 10),
        ("0", 0),
    ],
)
def test_intger_insert_normal(input_str, expected_value):
    moneymanagement = MoneyManagement()
    assert moneymanagement.isinteger_insert(input_str) == expected_value


@pytest.mark.parametrize(
    ("input_str", "expected_value"),
    [
        ("a", None),
        ("0.1", None),
        ("", None),
        ("```", None),
        ("\n", None),
    ],
)
def test_intger_insert_exception(input_str, expected_value):
    moneymanagement = MoneyManagement()
    assert moneymanagement.isinteger_insert(input_str) == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (10, 10),
        (50, 50),
        (100, 100),
        (500, 500),
        (1000, 1000),
    ],
)
def test_insert_coin_or_payout_normal(amount, expected_value):
    moneymanagement = MoneyManagement()
    moneymanagement.insert_coin_or_payout(amount)
    assert moneymanagement.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (2, False),  # 無効なお金
        ("a", False),  # 文字列
        (" ", False),  # 空白
        ("'''", False),  # 空文字
        (-1, False),  # 負の数
        (10000000000, False),  # ある程度大きい数ex.百億
        (0.1, False),  # 小数点
        ("\n", False),  # 改行
    ],
)
def test_insert_coin_or_payout_abnormal(amount, expected_value):
    moneymanagement = MoneyManagement()
    moneymanagement.insert_coin_or_payout(amount)
    assert moneymanagement.get_total_amount() == expected_value


class MockMoneyManagement:
    def __init__(self):
        self.total_entry_amount = 100

    def insert_coin_or_payout(self, amount):
        self.total_entry_amount += amount
        return self.total_entry_amount

    def get_total_amount(self):
        return self.total_entry_amount


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (0, 0),
        (100, 100),
        (500, 500),
    ],
)
def test_get_total_amount_normal(amount, expected_value):
    moneymanagement = MoneyManagement()
    moneymanagement.insert_coin_or_payout(amount)
    assert moneymanagement.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (0, 100),
        (100, 200),
        (500, 600),
    ],
)
def test_get_total_amount_add_normal(amount, expected_value):
    moneymanagement = MockMoneyManagement()
    moneymanagement.insert_coin_or_payout(amount)
    assert moneymanagement.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (10, "10円の釣り銭を返金します。"),
        (50, "50円の釣り銭を返金します。"),
        (100, "100円の釣り銭を返金します。"),
        (500, "500円の釣り銭を返金します。"),
        (1000, "1000円の釣り銭を返金します。"),
        (0, "0円の釣り銭を返金します。"),
    ],
)
def test_refund_normal(amount, expected_value):
    moneymanagement = MoneyManagement()
    moneymanagement.insert_coin_or_payout(amount)
    message = moneymanagement.refund()
    assert message == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (1, "このお金は受け付けられません。1円を返金します。"),
        (5, "このお金は受け付けられません。5円を返金します。"),
        (2000, "このお金は受け付けられません。2000円を返金します。"),
        (5000, "このお金は受け付けられません。5000円を返金します。"),
        (10000, "このお金は受け付けられません。10000円を返金します。"),
    ],
)
def test_money_exception_error(amount, expected_value):
    moneymanagement = MoneyManagement()
    message = moneymanagement.insert_coin_or_payout(amount)
    assert message == expected_value
