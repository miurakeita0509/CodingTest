import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.VendingMachine import VendingMachine
from src.JuiceManagement import JuiceManagement
from src.MoneyManagement import MoneyManagement
from src.SalesManagement import SalesManagement
from unittest.mock import Mock, patch


@pytest.mark.parametrize(
    ("input_str", "expected_value"),
    [
        ("10", 10),
        ("0", 0),
    ],
)
def test_intger_insert_normal(input_str, expected_value):
    vending_machine = VendingMachine()
    assert vending_machine.isinteger_amount(input_str) == expected_value


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
    vending_machine = VendingMachine()
    assert vending_machine.isinteger_amount(input_str) == expected_value


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
    vending_machine = VendingMachine()
    vending_machine.insert_coin_or_payout(amount)
    assert vending_machine.get_total_amount() == expected_value


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
    vending_machine = VendingMachine()
    vending_machine.insert_coin_or_payout(amount)
    assert vending_machine.get_total_amount() == expected_value


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
    vending_machine = VendingMachine()
    vending_machine.insert_coin_or_payout(amount)
    assert vending_machine.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (0, 100),
        (100, 200),
        (500, 600),
    ],
)
def test_get_total_amount_add_normal(amount, expected_value):
    vending_machine = MockMoneyManagement()
    vending_machine.insert_coin_or_payout(amount)
    assert vending_machine.get_total_amount() == expected_value


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
    vending_machine = VendingMachine()
    vending_machine.insert_coin_or_payout(amount)
    message = vending_machine.refund()
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
    vending_machine = VendingMachine()
    message = vending_machine.insert_coin_or_payout(amount)
    assert message == expected_value


@pytest.mark.parametrize(
    ("juice_name", "expected_value"),
    [
        (2, None),  # 無効なお金
        ("test", None),  # 文字列
        (" ", None),  # 空白
        ("'''", None),  # 空文字
        (-1, None),  # 負の数
        (10000000000, None),  # ある程度大きい数ex.百億
        (0.1, None),  # 小数点
        ("\n", None),  # 改行
    ],
)
def test_get_juice_info_abnormal(juice_name, expected_value):
    vending_machine = VendingMachine()
    assert vending_machine.get_juice_info(juice_name) == expected_value


@pytest.fixture
def vending_machine():
    Mock_vending_machine = VendingMachine()
    Mock_vending_machine.juice_management = Mock()
    Mock_vending_machine.money_management = Mock()
    Mock_vending_machine.sales_management = Mock()
    return Mock_vending_machine


@pytest.mark.parametrize(
    (
        "juice_name",
        "can_purchase_return",
        "price_return",
        "total_money",
        "expected_result",
    ),
    [
        ("コーラ", True, 120, 150, "コーラを購入しました。"),
        ("コーラ", False, 120, 100, "コーラは購入できません。"),
    ],
)
def test_purchase_normal(
    vending_machine,
    juice_name,
    can_purchase_return,
    price_return,
    total_money,
    expected_result,
):
    vending_machine.juice_management.can_purchase.return_value = can_purchase_return
    vending_machine.juice_management.get_juice_info.return_value = {
        "price": price_return
    }
    vending_machine.money_management.total_entry_amount = total_money
    result = vending_machine.purchase(juice_name)
    assert result == expected_result


@pytest.mark.parametrize(
    (
        "input_str",
        "juice_name",
        "show_juice_menu_return",
        "stock_return",
        "total_money",
        "expected_result",
    ),
    [
        ("1", "コーラ", {1: "コーラ"}, 0, 150, ("failed", "コーラ")),
    ],
)
def test_select_juice_purchase_no_stock(
    vending_machine,
    input_str,
    juice_name,
    show_juice_menu_return,
    stock_return,
    total_money,
    expected_result,
):
    with patch("builtins.input", side_effect=[input_str]):
        vending_machine.juice_management.show_juice_menu.return_value = (
            show_juice_menu_return
        )
        vending_machine.juice_management.get_juice_info.return_value = {
            "price": 120,
            "stock": stock_return,
        }
        vending_machine.money_management.total_entry_amount = total_money
        purchase_mock = Mock(return_value=f"{juice_name}は購入できません。")
        vending_machine.purchase = purchase_mock
        result = vending_machine.select_juice_purchase()
        assert result == expected_result
