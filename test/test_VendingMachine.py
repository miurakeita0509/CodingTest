import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.VendingMachine import VendingMachine
from src.VendingMachine import isinteger_insert
from src.VendingMachine import main
from src.VendingMachine import MENU_PROMPT


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
def test_insert_coin_or_payout_exception(amount, expected_value):
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


# UIのテストコード
@pytest.mark.parametrize(
    ("input_str", "exception_output"),
    [
        (
            "1\n" "50\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 50円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "a\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 無効な入力です。お金を入れてください。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
    ],
)
def test_main_selection1_normal(capsys, monkeypatch, input_str, exception_output):
    monkeypatch.setattr("sys.stdin", io.StringIO(input_str))
    main()
    # 標準出力のキャプチャを取得
    captured = capsys.readouterr()

    assert captured.out == exception_output


@pytest.mark.parametrize(
    ("input_str", "exception_output"),
    [
        (
            "2\n" "4\n",
            MENU_PROMPT + "投入金額の総計は0円です。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "10\n" "2\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 10円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "投入金額の総計は10円です。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "50\n" "2\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 50円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "投入金額の総計は50円です。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "100\n" "2\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 100円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "投入金額の総計は100円です。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "500\n" "2\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 500円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "投入金額の総計は500円です。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "1000\n" "2\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 1000円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "投入金額の総計は1000円です。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
    ],
)
def test_main_selection2_normal(capsys, monkeypatch, input_str, exception_output):
    monkeypatch.setattr("sys.stdin", io.StringIO(input_str))
    main()
    # 標準出力のキャプチャを取得
    captured = capsys.readouterr()

    assert captured.out == exception_output


@pytest.mark.parametrize(
    ("input_str", "exception_output"),
    [
        (
            "3\n" "4\n",
            MENU_PROMPT + "釣り銭はありません。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "1\n" "10\n" "3\n" "4\n",
            MENU_PROMPT + "お金を入れてください。: 10円を投入しました。\n"
            "\n\n" + MENU_PROMPT + "10円の釣り銭を返金します。\n"
            "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
    ],
)
def test_main_selection3_normal(capsys, monkeypatch, input_str, exception_output):
    monkeypatch.setattr("sys.stdin", io.StringIO(input_str))
    main()
    # 標準出力のキャプチャを取得
    captured = capsys.readouterr()

    assert captured.out == exception_output


@pytest.mark.parametrize(
    ("input_str", "exception_output"),
    [
        (
            "0\n" "4\n",
            MENU_PROMPT + "無効な選択肢です。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "a\n" "4\n",
            MENU_PROMPT + "無効な選択肢です。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            "'''\n" "4\n",
            MENU_PROMPT + "無効な選択肢です。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
        (
            " \n" "4\n",
            MENU_PROMPT + "無効な選択肢です。\n" "\n\n" + MENU_PROMPT + "自販機を終了します。\n",
        ),
    ],
)
def test_main_selection_normal(capsys, monkeypatch, input_str, exception_output):
    monkeypatch.setattr("sys.stdin", io.StringIO(input_str))
    main()
    # 標準出力のキャプチャを取得
    captured = capsys.readouterr()

    assert captured.out == exception_output
