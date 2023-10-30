from VendingMachine import VendingMachine, isinteger_insert
from JuiceManagement import JuiceManagement

MENU_PROMPT = (
    "メニュー:\n"
    "1. お金を投入します。\n"
    "2. 総計を確認します。\n"
    "3. 払い戻しをします。\n"
    "4. 取扱ドリンク\n"
    "5. 売り上げを確認します。\n"
    "6. 終了します。\n"
    "選択肢を入力してください。: "
)


def main():
    # 自販機を作成
    creation_vending_machine = VendingMachine()
    juice_management = JuiceManagement()

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
            while True:
                status, selected_juice = creation_vending_machine.select_juice_purchase(
                    juice_management
                )
                if status == "success":
                    print(f"{selected_juice}を購入しました。")
                    break
                elif status == "failed":
                    print(f"{selected_juice}は購入できません。再度選択してください。")
                elif status == "cancel":
                    break
                elif status == "invalid_select":
                    print("無効な選択です。再度選択してください。")

        elif selection == "5":
            current_sales = juice_management.get_sales()
            print(f"現在の売上は{current_sales}円です。")
        elif selection == "6":
            print("自販機を終了します。")
            break
        else:
            print("無効な選択肢です。")
        print("\n")


if __name__ == "__main__":  # pragma: no cover
    main()
