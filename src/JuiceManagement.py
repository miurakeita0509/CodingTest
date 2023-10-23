class JuiceManagement:
    def __init__(self):
        self.juice = {
            "cola": {"name": "コーラ", "price": 120, "stock": 5},
        }

    def get_juice_info(self, juice_name=None):
        if juice_name:
            return self.juice.get(juice_name)
        return self.juice
