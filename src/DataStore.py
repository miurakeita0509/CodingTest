class DataStore:
    def __init__(self):
        self.sales = 0

    # ジュースの購入の売上
    def record_juice_sales(self, juice_management, juice_name):
        if juice_management.get_juice_info(juice_name):
            self.sales += juice_management.juice[juice_name]["price"]
            return True
        return False

    # 売上を返す
    def get_sales(self):
        return self.sales
