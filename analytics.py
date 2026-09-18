# analytics.py - running balance, flagging, duplicate and outlier detection, and category totals for a list of transaction onjects

# generator - yields the balance after each transactioin 
def running_balance(transactions, start=0.0):
    balance = start
    for transaction in transactions:
        balance += transactions.amount
        yield balance


