# step1 自販機お金の処理
# step2 自販機は扱えないお金を弾くことができる
MENU_PROMPT = (
    "メニュー:\n"
    "1. お金を投入します。\n"
    "2. 総計を確認します。\n"
    "3. 払い戻しをします。\n"
    "4. 終了します。\n"
    "選択肢を入力してください。: "
)


class VendingMachine:
    # 投入金額の総計
    def __init__(self):
        self.total_entry_amount = 0

    # 10円玉、50円玉、100円玉、500円玉、1000円札を受け付ける
    def insert_coin_or_payout(self, amount_integer):
        if amount_integer in [10, 50, 100, 500, 1000]:
            self.total_entry_amount += amount_integer
            return f"{amount_integer}円を投入しました。"
        elif amount_integer in [1, 5, 2000, 5000, 10000]:  # 実在するお金
            return f"このお金は受け付けられません。{amount_integer}円を返金します。"
        else:
            return "無効なお金です。"

    # 投入金額の総計を取得
    def get_total_amount(self):
        return self.total_entry_amount

    # 釣り銭を出力
    def refund(self):
        if self.total_entry_amount > 0:
            temporary_storing = self.total_entry_amount
            self.total_entry_amount = 0
            return f"{temporary_storing}円の釣り銭を返金します。"
        else:
            return "釣り銭はありません。"


def isinteger_insert(amount):
    try:
        return int(amount)
    except ValueError:
        return None


def main():
    # 自販機を作成
    creation_vending_machine = VendingMachine()

    while True:
        print(MENU_PROMPT, end="")
        selection = input()

        if selection == "1":
            amount = input("お金を入れてください。: ")
            amount_integer = isinteger_insert(amount)

            if amount_integer is None:
                print("無効な入力です。お金を入れてください。")
            else:
                print(creation_vending_machine.insert_coin_or_payout(amount_integer))
        elif selection == "2":
            total_entry_amount = creation_vending_machine.get_total_amount()
            print(f"投入金額の総計は{total_entry_amount}円です。")
        elif selection == "3":
            print(creation_vending_machine.refund())
        elif selection == "4":
            print("自販機を終了します。")
            break
        else:
            print("無効な選択肢です。")
        print("\n")


if __name__ == "__main__":  # pragma: no cover
    main()
