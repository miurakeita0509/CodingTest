import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.VendingMachine import VendingMachine, isinteger_insert
from src.main import main, MENU_PROMPT


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
