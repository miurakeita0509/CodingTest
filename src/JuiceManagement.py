class JuiceManagement:
    def __init__(self):
        self.juice = {
            "コーラ": {"name": "コーラ", "price": 120, "stock": 5},
        }

    # ジュースの情報を返す
    def get_juice_info(self, juice_name=None):
        if juice_name:
            return self.juice.get(juice_name)
        return self.juice

    # step4の1行目
    def can_purchase(self, juice_name, amount):
        juice = self.get_juice_info(juice_name)
        if not juice:
            return False  # ジュースが存在しない
        return (amount >= juice["price"]) and (juice["stock"] > 0)

    # step4の2行目 在庫を減らす
    def decrease_juice_stock(self, juice_name):
        if self.juice[juice_name]["stock"] > 0:
            self.juice[juice_name]["stock"] -= 1
            return True
        return False

    # 購入可能かどうかの表示
    def show_juice_menu(self, money_management):
        avairable_juice = self.get_juice_info()
        index_name_map = {}
        print("0. 購入をやめますか？")
        for index, (name, juice) in enumerate(avairable_juice.items(), 1):
            if (
                money_management.get_total_amount() >= juice["price"]
                and juice["stock"] > 0
            ):
                status = "購入可能です。"
            elif juice["stock"] == 0:
                status = "在庫がありません。"
            else:
                status = "投入金額が足りません。"
            print(f"{index}.{name}:{status}")
            index_name_map[index] = name
        return index_name_map
