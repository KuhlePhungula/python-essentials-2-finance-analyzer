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
        "2026-08-01,Grocery Store,-54.30,Food",         # duplicate
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


