import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.JuiceManagement import JuiceManagement


@pytest.mark.parametrize(
    ("juice_name", "expected_value"),
    [
        ("コーラ", {"name": "コーラ", "price": 120, "stock": 5}),
    ],
)
def test_get_juice_info_normal(juice_name, expected_value):
    juice_management = JuiceManagement()
    assert juice_management.get_juice_info(juice_name) == expected_value


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
    juice_management = JuiceManagement()
    assert juice_management.get_juice_info(juice_name) == expected_value


@pytest.mark.parametrize(
    ("juice_name", "amount", "expected_value"),
    [
        ("コーラ", 100, False),  # 在庫5の状態かつ投入金額が下回ってる場合
        ("コーラ", 120, True),  # 在庫5の状態かつ投入金額が同値の場合
        ("コーラ", 130, True),  # 在庫5の状態かつ投入金額が上回ってる場合
        ("コーラ", 150, False),  # 在庫0の状態
        ("無名なジュース", 140, None),  # クラスに該当する名前がない場合
    ],
)
def test_can_purchase_normal(juice_name, amount, expected_value):
    juice_management = JuiceManagement()
    if juice_name == "コーラ" and amount == 150:
        juice_management.juice["コーラ"]["stock"] = 0
    assert juice_management.can_purchase(juice_name, amount) == expected_value


@pytest.mark.parametrize(
    ("juice_name", "amount", "expected_value"),
    [
        ("コーラ", 100, True),
        ("コーラ", 150, False),
    ],
)
def test_decrease_juice_stock_normal(juice_name, amount, expected_value):
    juice_management = JuiceManagement()
    if juice_name == "コーラ" and amount == 150:
        juice_management.juice["コーラ"]["stock"] = 0
    assert juice_management.decrease_juice_stock(juice_name) == expected_value


class MockMoneyManagement:
    def __init__(self, amount):
        self.total_entry_amount = amount

    def get_total_amount(self):
        return self.total_entry_amount


@pytest.mark.parametrize(
    ("amount", "expected_output"),
    [
        (100, "0. 購入をやめますか？\n1.コーラ:投入金額が足りません。\n"),
        (120, "0. 購入をやめますか？\n1.コーラ:購入可能です。\n"),
        (130, "0. 購入をやめますか？\n1.コーラ:購入可能です。\n"),
        (150, "0. 購入をやめますか？\n1.コーラ:在庫がありません。\n"),
    ],
)
def test_show_juice_menu_normal(amount, expected_output):
    juice_management = JuiceManagement()
    if amount == 150:
        juice_management.juice["コーラ"]["stock"] = 0
    mock_money_management = MockMoneyManagement(amount)
    sys.stdout = io.StringIO()
    juice_management.show_juice_menu(mock_money_management)
    captured_out = sys.stdout.getvalue()
    assert captured_out == expected_output
