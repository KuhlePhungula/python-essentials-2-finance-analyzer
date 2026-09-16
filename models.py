# Transaction class, featuring date, description, amount, and category, for a siingle transaction

class Transaction:
    # class variable
    count = 0

    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.category = category

