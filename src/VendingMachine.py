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

    # ジュースの購入
    def purchase(self, juice_name, juice_management):
        if juice_management.can_purchase(juice_name, self.total_entry_amount):
            juice_price = juice_management.get_juice_info(juice_name)["price"]
            self.total_entry_amount -= juice_price
            juice_management.purchase_juice(juice_name)
            return f"{juice_name}を購入しました。"
        else:
            return f"{juice_name}は購入できません。"

    def select_juice_purchase(self, juice_management):
        while True:
            print("\n")
            index_name_map = juice_management.show_juice_menu(self)
            select = input("どのドリンクを購入しますか。: ")
            if select.isdigit() and int(select) == 0:
                print("購入をやめます。")
                return "cancel", None
            if select.isdigit() and int(select) in index_name_map:
                selected_juice = index_name_map[int(select)]
                result = self.purchase(selected_juice, juice_management)
                if "購入しました。" in result:
                    return "success", selected_juice
                else:
                    return "failed", selected_juice
            else:
                return "invalid_select", None


def isinteger_insert(amount):
    try:
        return int(amount)
    except ValueError:
        return None
