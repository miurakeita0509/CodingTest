import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.VendingMachine import VendingMachine, isinteger_insert
from src.main import main, MENU_PROMPT


# ロジックのテストコード
@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        # 正常系入力
        (10, 10),
        (50, 50),
        (100, 100),
        (500, 500),
        (1000, 1000),
    ],
)
def test_insert_coin_or_payout_normal(amount, expected_value):
    vm = VendingMachine()
    vm.insert_coin_or_payout(amount)
    assert vm.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        # 異常系入力
        (2, 0),  # 無効なお金
        ("a", 0),  # 文字列
        (" ", 0),  # 空白
        ("'''", 0),  # 空文字
        (-1, 0),  # 負の数
        (10000000000, 0),  # ある程度大きい数ex.百億
        (0.1, 0),  # 小数点
    ],
)
def test_insert_coin_or_payout_abnormal(amount, expected_value):
    vm = VendingMachine()
    vm.insert_coin_or_payout(amount)
    assert vm.get_total_amount() == expected_value


@pytest.mark.parametrize(
    ("amount", "expected_value"),
    [
        (100, 0),
        (500, 0),
        (0, 0),
    ],
)
def test_refund_normal(amount, expected_value):
    vm = VendingMachine()
    vm.insert_coin_or_payout(amount)
    vm.refund()
    assert vm.get_total_amount() == expected_value


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
    vm = VendingMachine()
    message = vm.insert_coin_or_payout(amount)
    assert message == expected_value


@pytest.mark.parametrize(
    ("input_str", "expected_value"),
    [
        ("10", 10),
        ("0", 0),
    ],
)
def test_intger_insert_normal(input_str, expected_value):
    assert isinteger_insert(input_str) == expected_value


@pytest.mark.parametrize(
    "input_str",
    [
        "a",
        "0.1",
        "",
        " ",
        "'''",
    ],
)
def test_intger_insert_exception(input_str):
    assert isinteger_insert(input_str) is None
