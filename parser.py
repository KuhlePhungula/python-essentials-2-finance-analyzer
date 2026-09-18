# Defensive loading of transaction data from a statement file.

import os
from datetime import datetime
from models import Transaction

sample_file_path = "data/statement.txt"

# write a sample file that intentionally includes every broken case
def generate_sample_file(path=sample_file_path):

    lines = [
        "2026-08-01,Grocery Store,-54.80,Food",
        "2026-07-25,Monthly Salary,2500,Salary",
        "2026/08/03,Coffee Shop,-4.75,Food",        # slash date format
        "2026-08-04;Electric Bill;-89.10;Bills",    # wrong separator
        "2026-08-05,Refund,150.00",                 # missing category field
        "not a transaction line at all",            # junk line
        "2026-08-06,Bookstore,twelve,Entertainment",    # non-numeric amount
        "2026-08-01,Grocery Store,-54.80,Food",         # duplicate
        "2026-08-07,Freelance Payment,-300.00,Freelance",       # sign and category mismatch
        "  2026-08-08 ,  Gym Membership , -40.00 , Health  ",   # blank space
        "2026-08-09,Holiday Bonus,150.00,Bonus",
        "2026-08-10,Restaurant,-22.50,Food",
        "2026-02-30,Rent,-900.00,Bills",            # impossible date
        "2026-08-11,,-25.00,Shopping",              # missing description
        "2026-08-12,Mystery Fee,nan,Bills",         # non-infinte amount


    ]

    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")

# correcting wrong date and wrong date format
def normalize_date(raw_date):

    cleaned = raw_date.strip().replace("/", "-")
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"'{raw_date.strip()}' is not a valid date")
    return parsed.strftime("%Y-%m-%d")

# read statement file and return (transactions, rejected)
def load_transactions(path):

    transactions = []
    rejections = []

    try:
        with open(path, "r") as f:
            raw_lines = f.readlines()
    except FileNotFoundError:
        print(f"Could not find statement file: {path}")
        return transactions, [f"file not found: {path}"]

    if len(raw_lines) == 0:
        print(f"Statement file is empty: {path}")
        return transactions, [f"file is empty: {path}"]

    for row_number, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()

        if line == "":
            continue

        try:
            fields = line.split(",")
            if len(fields) != 4:
                raise ValueError(f"Expected 4 fields, got {len(fields)}")

            date_str = normalize_date(fields[0])

            description = fields[1].strip()
            if description == "":
                raise ValueError("Description is empty.")

            amount = float(fields[2].strip())
            if amount != amount or abs(amount) == float("inf"):
                raise ValueError(f"'{fields[2].strip()}' is not a valid number")

            category = fields[3].strip()
            if category == "":
                raise ValueError("Category is empty.")

            transactions.append(Transaction(date_str, description, amount, category))

        except ValueError as error:
            rejections.append(f"row {row_number}: {error}")
        except Exception as error:
            rejections.append(f"Row {row_number}: unexpected error - {error}")

    return transactions, rejections

if __name__ == "___main__":
    generate_sample_file()
    valid_transactions, rejected_rows = load_transactions(sample_file_path)

    print(f"{len(valid_transactions)} transactions loaded successfully.")
    print(f"{len(rejected_rows)} rows rejected:")
    for reason in rejected_rows:
        print(f" - {reason}")
