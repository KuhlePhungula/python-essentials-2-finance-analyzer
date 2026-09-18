# analytics.py - running balance, flagging, duplicate and outlier detection, and category totals for a list of transaction onjects

# generator - yields the balance after each transactioin 
def running_balance(transactions, start=0.0):
    balance = start
    for transaction in transactions:
        balance += transactions.amount
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

