from VendingMachine import VendingMachine


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
    vending_machine = VendingMachine()

    while True:
        print(MENU_PROMPT, end="")
        selection = input()

        # お金の投入
        if selection == "1":
            amount = input("お金を入れてください。: ")
            amount_integer = vending_machine.isinteger_amount(amount)
            if amount_integer is None:
                print("無効な入力です。お金を入れてください。")
            else:
                print(vending_machine.insert_coin_or_payout(amount_integer))

        # 総計の確認
        elif selection == "2":
            total_entry_amount = vending_machine.get_total_amount()
            print(f"投入金額の総計は{total_entry_amount}円です。")

        # 売上の確認
        elif selection == "3":
            print(vending_machine.refund())

        # 取扱ドリンクの購入可否
        elif selection == "4":
            while True:
                status, selected_juice = vending_machine.select_juice_purchase()
                if status == "success":
                    print(f"{selected_juice}を購入しました。")
                    print(vending_machine.refund())
                    break
                elif status == "failed":
                    print(f"{selected_juice}は購入できません。再度選択してください。")
                elif status == "cancel":
                    print("購入をやめます。")
                    break
                elif status == "invalid_select":
                    print("無効な選択です。再度選択してください。")

        # 売上の確認
        elif selection == "5":
            current_sales = vending_machine.get_sales()
            print(f"現在の売上は{current_sales}円です。")

        # 自販機の終了
        elif selection == "6":
            print("自販機を終了します。")
            break
        else:
            print("無効な選択肢です。")
        print("\n")


if __name__ == "__main__":  # pragma: no cover
    main()
