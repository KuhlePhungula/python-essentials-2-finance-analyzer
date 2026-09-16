# Transaction class, featuring date, description, amount, and category, for a siingle transaction

class Transaction:
    # class variable
    count = 0

    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.category = category

    # retuens True if the transaction is money coming in
    def is_income(self):
        return self.amount > 0

    # formatted method returning a simple one line transaction daya
    def formatted(self):
        sign = "+" if self.amount >= 0 else "-"
        return f"{self.date} {self.description} {sign}{abs(self.amount):.2f} {self.category}"

    def __str__(self):
        kind = "Income" if self.is_income() else "Expense"
        return f"[{kind}] {self.date} | {self.description} | {self.amount:.2f} | {self.category}"
    

