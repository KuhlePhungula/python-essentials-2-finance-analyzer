# Transaction class, featuring date, description, amount, and category, for a slingle transaction

class Transaction:
    # class variable: counting how many transactions are created
    count = 0

    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.category = category

        Transaction.count += 1

    # returns True if the transaction is money coming in
    def is_income(self):
        return self.amount > 0

    # formatted method returning a simple one line transaction data
    def formatted(self):
        sign = "+" if self.amount >= 0 else "-"
        return f"{self.date} {self.description} {sign}{abs(self.amount):.2f} {self.category}"

    def __str__(self):
        kind = "Income" if self.is_income() else "Expense"
        return f"[{kind}] {self.date} | {self.description} | {self.amount:.2f} | {self.category}"


# Transaction subclass that repeats on a fixed interval, for example a subscription or rent 
class RecurringTransaction(Transaction):

    def __init__(self, date, description, amount, category, interval):
        super().__init__(date, description, amount, category)
        self.interval = interval

    def formatted(self):
        line = super().formatted()
        return f"{line} (recurring: {self.interval})"

    def __str__(self):
        line = super().__str__()
        return f"{line} | recurring: {self.interval}"

    



