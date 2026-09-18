# reporting.py - write the analyzer's report and run log

import os 
import platform
from datetime import datetime
from analytics import category_totals, find_duplicates, find_outliers, running_balance

report_path = "data/report.txt"
log_path = "data/run_log.txt"

income_categories = {"income", "salary", "freelance", "bonus", "refund", "gift"}
expense_categories = {"expense", "food", "entertainment", "transport", "rent", "bills", "shopping", "health", "subscriptions"}

# one line describing when and wherethe analyzer ran
def environment_timestamp():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Run at {now} on {platform.system()} {platform.release()} (Python {platform.python_version()})"

# flag transaction whose amount sign doesn't match what their category implies
def find_inconsistent_transactions(transactions):
    inconsistent = []
    for transaction in transactions:
        category = transaction.category.lower()
        if category in income_categories and transaction.amount < 0:
            inconsistent.append(transaction)
        elif category in expense_categories and transaction.amount > 0:
            inconsistent.append(transaction)
    return inconsistent



