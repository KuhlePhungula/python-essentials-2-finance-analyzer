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

# writes a summary report to path covering totals, category breakdown, rejected rows, duplicates, outliers, and sign mismatches
def monthly_summary(transactions, rejections=None, path=report_path):
    if rejections is None:
        rejections = []

    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    totals = category_totals(transactions)
    duplicates = find_duplicates(transactions)
    outliers = find_outliers(transactions)
    inconsistent = find_inconsistent_transactions(transactions)

    final_balance = 0.0
    for balance in running_balance(transactions):
        final_balance = balance

    lines = []
    lines.append("===== MONTHLY SUMMARY REPORT =====")
    lines.append(environment_timestamp())
    lines.append("")
    lines.append(f"Transactions loaded: {len(transactions)}")
    lines.append(f"Rows rejected: {len(rejections)}")
    lines.append(f"Final balance: {final_balance:.2f}")
    lines.append("")

    lines.append("Category breakdown:")
    for category, total in totals.items():
        lines.append(f"{category}: {total:.2f}")
    lines.append("")

    lines.append(f"Duplicate transactions found: {len(duplicates)}")
    for transaction in duplicates:
        lines.append(f"{transaction.formatted()}")
    lines.append("")

    lines.append(f"Unusual transactions (outliers) found: {len(outliers)}")
    for transaction in outliers:
        lines.append(f"{transaction.formatted()}")
    lines.append("")

    lines.append(f"Sign/category mismatches found: {len(inconsistent)}")
    for transaction in inconsistent:
        lines.append(f"{transaction.formatted()}")
    lines.append("")

    if rejections:
        lines.append("Rejected rows:")
        for reason in rejections:
            lines.append(f"{reason}")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    _log_run(len(transactions), len(rejections), len(duplicates), len(outliers), len(inconsistent))

    return path

# append one line per analyzer run to an ongoing file
def _log_run(loaded_count, rejected_count, duplicate_count, outlier_count, inconsistent_count):
    folder = os.path.dirname(log_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{stamp} | loaded = {loaded_count} rejected = {rejected_count} "
        f"duplicates = {duplicate_count} outliers = {outlier_count} "
        f"inconsistent = {inconsistent_count}\n"
    )

    with open(log_path, "a") as f:
        f.write(line)

