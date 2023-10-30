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
        "コーラ": {"name": "コーラ", "price": 120, "stock": 5},
    }
    assert jm.get_juice_info() == expected_juices


@pytest.mark.parametrize(
    ("juice", "expected_value"),
    [
        ("コーラ", {"name": "コーラ", "price": 120, "stock": 5}),
    ],
)
def test_get_juice_info_normal(juice, expected_value):
    jm = JuiceManagement()
    assert jm.get_juice_info(juice) == expected_value


@pytest.mark.parametrize(
    ("juice", "expected_value"),
    [
        (2, None),  # 無効なお金
        ("test", None),  # 文字列
        (" ", None),  # 空白
        ("'''", None),  # 空文字
        (-1, None),  # 負の数
        (10000000000, None),  # ある程度大きい数ex.百億
        (0.1, None),  # 小数点
    ],
)
def test_get_juice_info_abnormal(juice, expected_value):
    jm = JuiceManagement()
    assert jm.get_juice_info(juice) == expected_value


@pytest.mark.parametrize(
    ("juice_name", "amount", "expected_value"),
    [
        ("コーラ", 100, False),  # 在庫5の状態かつ投入金額が下回ってる場合
        ("コーラ", 120, True),  # 在庫5の状態かつ投入金額が同値の場合
        ("コーラ", 130, True),  # 在庫5の状態かつ投入金額が上回ってる場合
        ("コーラ", 150, False),  # 在庫0の状態
        ("無名なジュース", 140, False),  # クラスに該当する名前がない場合
    ],
)
def test_can_purchase_normal(juice_name, amount, expected_value):
    jm = JuiceManagement()
    if juice_name == "コーラ" and amount == 150:
        jm.juice["コーラ"]["stock"] = 0
    assert jm.can_purchase(juice_name, amount) == expected_value


@pytest.mark.parametrize(
    ("juice_name", "expected_value"),
    [
        ("コーラ", True),
    ],
)
def test_purchase_juice_normal_true(juice_name, expected_value):
    jm = JuiceManagement()
    assert jm.purchase_juice(juice_name) == expected_value


@pytest.mark.parametrize(
    ("juice_name", "expected_value"),
    [
        ("コーラ", False),
    ],
)
def test_purchase_juice_normal_false(juice_name, expected_value):
    jm = JuiceManagement()
    for _ in range(6):
        jm.purchase_juice("コーラ")
    assert jm.purchase_juice(juice_name) == expected_value


def test_get_sales():
    jm = JuiceManagement()
    assert jm.get_sales() == 0
    jm.purchase_juice("コーラ")
    assert jm.get_sales() == 120
    jm.purchase_juice("コーラ")
    assert jm.get_sales() == 120 * 2


class MockVendingMachine:
    def __init__(self, amount):
        self.amount = amount

    def get_total_amount(self):
        return self.amount


@pytest.mark.parametrize(
    ("amount", "exception_output"),
    [
        (100, "0. 購入をやめますか？\n1.コーラ:投入金額が足りません。\n"),
        (120, "0. 購入をやめますか？\n1.コーラ:購入可能です。\n"),
        (130, "0. 購入をやめますか？\n1.コーラ:購入可能です。\n"),
        (150, "0. 購入をやめますか？\n1.コーラ:在庫がありません。\n"),
    ],
)
def test_show_juice_menu_normal(amount, exception_output):
    jm = JuiceManagement()
    if amount == 150:
        jm.juice["コーラ"]["stock"] = 0
    Mock_vm = MockVendingMachine(amount)
    sys.stdout = io.StringIO()
    jm.show_juice_menu(Mock_vm)
    captured_out = sys.stdout.getvalue()

    assert captured_out == exception_output
