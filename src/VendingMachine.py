from JuiceManagement import JuiceManagement
from MoneyManagement import MoneyManagement
from SalesManagement import SalesManagement


class VendingMachine:
    def __init__(self):
        self.juice_management = JuiceManagement()
        self.money_management = MoneyManagement()
        self.sales_management = SalesManagement()

    # 整数選定
    def isinteger_amount(self, amount):
        return self.money_management.isinteger_insert(amount)

    # 10円玉、50円玉、100円玉、500円玉、1000円札を受け付ける
    def insert_coin_or_payout(self, amount_integer):
        return self.money_management.insert_coin_or_payout(amount_integer)

    # 投入金額の総計を取得
    def get_total_amount(self):
        return self.money_management.get_total_amount()

    # 釣り銭を出力
    def refund(self):
        return self.money_management.refund()

    # 売上を返す
    def get_sales(self):
        return self.sales_management.get_sales()

    # ジュースの情報を返す
    def get_juice_info(self, juice_name):
        return self.juice_management.get_juice_info(juice_name)

    # ジュースの購入
    def purchase(self, juice_name):
        if self.juice_management.can_purchase(
            juice_name, self.money_management.total_entry_amount
        ):
            juice_price = self.juice_management.get_juice_info(juice_name)["price"]
            self.money_management.total_entry_amount -= juice_price
            self.juice_management.decrease_juice_stock(juice_name)
            self.sales_management.record_juice_sales(juice_price)
            return f"{juice_name}を購入しました。"
        else:
            return f"{juice_name}は購入できません。"

    def select_juice_purchase(self):
        while True:
            print("\n")
            index_name_map = self.juice_management.show_juice_menu(
                self.money_management.get_total_amount()
            )
            select = input("どのドリンクを購入しますか。: ")
            if select.isdigit() and int(select) == 0:
                return "cancel", None
            if select.isdigit() and int(select) in index_name_map:
                selected_juice = index_name_map[int(select)]
                result = self.purchase(selected_juice)
                if "購入しました。" in result:
                    return "success", selected_juice
                else:
                    return "failed", selected_juice
            else:
                return "invalid_select", None
