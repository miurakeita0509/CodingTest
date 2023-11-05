class JuiceManagement:
    def __init__(self):
        self.juice = {
            "コーラ": {"name": "コーラ", "price": 120, "stock": 5},
            "レッドブル": {"name": "レッドブル", "price": 200, "stock": 5},
            "水": {"name": "水", "price": 100, "stock": 5},
        }

    # ジュースの情報を返す
    def get_juice_info(self, juice_name=None):
        if juice_name:
            return self.juice.get(juice_name)
        return self.juice

    # 投入金額、在庫の点で、コーラが購入できるかどうか
    def can_purchase(self, juice_name, amount):
        juice = self.get_juice_info(juice_name)
        if not juice:
            return None  # ジュースが存在しない
        trueorfalse = (amount >= juice["price"]) and (juice["stock"] > 0)
        return trueorfalse

    # 在庫を減らす
    def decrease_juice_stock(self, juice_name):
        if self.juice[juice_name]["stock"] > 0:
            self.juice[juice_name]["stock"] -= 1
            return True
        return False

    # 購入可能かどうかの表示
    def show_juice_menu(self, total_amount):
        available_juice = self.get_juice_info()
        index_name_map = {}
        print("0. 購入をやめますか？")
        for index, (name, juice) in enumerate(available_juice.items(), 1):
            juice_price = juice["price"]
            if total_amount >= juice["price"] and juice["stock"] > 0:
                status = "購入可能です。"
            elif juice["stock"] == 0:
                status = "在庫がありません。"
            else:
                status = "投入金額が足りません。"
            print(f"{index}.{name} {juice_price}円 : {status}")
            index_name_map[index] = name
        return index_name_map
