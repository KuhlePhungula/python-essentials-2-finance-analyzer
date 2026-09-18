# analytics.py - running balance, flagging, duplicate and outlier detection, and category totals for a list of transaction onjects

# generator - yields the balance after each transactioin 
def running_balance(transactions, start=0.0):
    balance = start
    for transaction in transactions:
        balance += transaction.amount
        yield balance

# closure - returns a function that flags any transaction whose amount magnitude is bigger than the remembered threshold
def make_flagger(threshold):
    def flagger(transaction):
        return abs(transaction.amount) > threshold

    return flagger

# return every transaction that repeats an earlier exact match, using a set of signatures to spot repeats
def find_duplicates(transactions):
    seen = set()
    duplicates = []

    for transaction in transactions:
        signature = (
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.category
        )
        if signature in seen:
            duplicates.append(transaction)
        else:
            seen.add(signature)
    return duplicates


def find_outliers(transactions, num_std_devs=2):
    if len(transactions) < 2:
        return []

    amounts = [transaction.amount for transaction in transactions]
    mean = sum(amounts) / len(amounts)

    variance = sum((amount - mean) ** 2 for amount in amounts) / len(amounts)
    std_dev = variance ** 0.5

    if std_dev == 0:
        return []

    outliers = []
    for transaction in transactions:
        distance = abs(transaction.amount - mean) / std_dev
        if distance > num_std_devs:
            outliers.append(transaction)

    return outliers

# sum the amounts in each category
def category_totals(transactions):
    totals = {}
    for transaction in transactions:
        category = transaction.category
        totals[category] = totals.get(category, 0.0) + transaction.amount
    return totals