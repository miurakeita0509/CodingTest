class MoneyManagement:
    # 投入金額の総計
    def __init__(self):
        self.total_entry_amount = 0

    # 整数選定
    def isinteger_insert(self, amount):
        try:
            return int(amount)
        except ValueError:
            return None

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
