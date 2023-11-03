class SalesManagement:
    def __init__(self):
        self.sales = 0

    # ジュースの購入の売上
    def record_juice_sales(self, juice_price):
        self.sales += juice_price
        return True

    # 売上を返す
    def get_sales(self):
        return self.sales
