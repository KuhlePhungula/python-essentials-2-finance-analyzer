# self-tests for the finance analyzer

import os
from models import Transaction, RecurringTransaction
from parser import generate_sample_file, load_transactions, sample_file_path, normalize_date
from analytics import running_balance, make_flagger, find_duplicates, category_totals
from reporting import find_inconsistent_transactions

def test_valid_row_parses_correctly():
    transaction = Transaction("2026-08-01", "Groceries", -50.0, "FOOD")
    assert transaction.date == "2026-08-01", "date not stored correctly"
    assert isinstance(transaction.amount, float), "amount should be stored as a float"
    assert transaction.amount == -50.0, "amount value is wrong"
    assert transaction.category == "FOOD", "category not stored correctly"

def test_is_income():
    income = Transaction("2026-08-01", "Salary", 1000.0, "Income")
    expense = Transaction("2026-08-01", "Rent", -900.0, "Expense")
    assert income.is_income() is True, "a positive amount should be income"
    assert expense.is_income() is False, "a negative amount should not be income"

def test_transaction_count_increments():
    count_before = Transaction.count
    Transaction("2026-08-01", "Test A", -10.0, "Expense")
    Transaction("2026-08-02", "Test B", 20.0, "Income")
    count_after = Transaction.count
    assert count_after - count_before == 2, "Transaction.count should go up by 2 after creating 2 transactions"

def test_recurring_transaction_override():
    recurring = RecurringTransaction("2026-08-01", "Netflix", -15.0, "Entertainment", "monthly")
    assert isinstance(recurring, Transaction), "RecurringTransaction should inherit from Transaction"
    assert "recurring" in recurring.formatted().lower(), "formatted() override should mention the recurring interval"
    assert "monthly" in str(recurring), "__str__ override should include the interval"

def test_normalize_date_validates_real_dates():
    assert normalize_date("2026/08/03") == "2026-08-03", "should normalize slash separators to dashes"
    try:
        normalize_date("2026-02-30")
        assert False, "an impossible calendar date should raise ValueError"
    except ValueError:
        pass

def test_loader_parses_valid_row():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    matches = [t for t in transactions if t.date == "2026-08-01" and t.description == "Grocery Store"]
    assert len(matches) >= 1, "the first valid row should have loaded"
    matched = matches[0]
    assert isinstance(matched.amount, float), "amount should be parsed as a float"
    assert matched.amount == -54.80, "amount was not parsed correctly"
    assert matched.category == "Food", "category was not parsed correctly"

def test_loader_normalizes_slash_dates():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    dates = [t.date for t in transactions]
    assert "2026-08-03" in dates, "slash-formatted date should be normalized, not rejected"
    assert "2026/08/03" not in dates, "date should not keep its original slash format"

def test_loader_rejects_junk_and_missing_fields():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    descriptions = [t.description for t in transactions]
    assert "Refund" not in descriptions, "row missing a field should be rejected"
    assert len(rejections) >= 2, "the junk line and missing-field row should both be rejected"

def test_loader_rejects_non_numeric_amount():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    descriptions = [t.description for t in transactions]
    assert "Bookstore" not in descriptions, "row with a non-numeric amount should be rejected"

def test_loader_rejects_invalid_calendar_date():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    descriptions = [t.description for t in transactions]
    assert "Rent" not in descriptions, "a row with an impossible calendar date (Feb 30) should be rejected"

def test_loader_rejects_non_finite_amount():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    descriptions = [t.description for t in transactions]
    assert "Mystery Fee" not in descriptions, "a non-finite amount like nan should be rejected"

def test_loader_rejects_empty_field():
    generate_sample_file()
    transactions, rejections = load_transactions(sample_file_path)
    empty_description_rows = [t for t in transactions if t.description == ""]
    assert empty_description_rows == [], "a row with an empty description should be rejected"

def test_loader_handles_missing_file():
    transactions, rejections = load_transactions("data/does_not_exist.txt")
    assert transactions == [], "a missing file should load zero transactions"
    assert len(rejections) == 1, "a missing file should report exactly one rejection reason"

def test_loader_handles_empty_file():
    empty_path = "data/empty_statement.txt"
    folder = os.path.dirname(empty_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    open(empty_path, "w").close()
 
    transactions, rejections = load_transactions(empty_path)
    assert transactions == [], "an empty file should load zero transactions"
    assert len(rejections) == 1, "an empty file should report exactly one rejection reason"

def test_running_balance_sequence():
    sample = [
        Transaction("2026-08-01", "Salary", 1000.0, "Salary"),
        Transaction("2026-08-02", "Rent", -400.0, "Bills"),
        Transaction("2026-08-03", "Groceries", -100.0, "Food"),
    ]
    balances = list(running_balance(sample, start=0.0))
    assert balances == [1000.0, 600.0, 500.0], "running_balance gave the wrong sequence"

def test_make_flagger():
    big = Transaction("2026-08-01", "New Laptop", -5000.0, "Shopping")
    small = Transaction("2026-08-01", "Coffee", -50.0, "Food")
    flag = make_flagger(1000)
    assert flag(big) is True, "a 5000 transaction should be flagged with a 1000 threshold"
    assert flag(small) is False, "a 50 transaction should not be flagged with a 1000 threshold"

def test_find_duplicates_detects_planted_duplicate():
    sample = [
        Transaction("2026-08-01", "Groceries", -50.0, "Food"),
        Transaction("2026-08-01", "Groceries", -50.0, "Food"),
        Transaction("2026-08-02", "Salary", 1000.0, "Salary"),
    ]
    duplicates = find_duplicates(sample)
    assert len(duplicates) == 1, "should find exactly one duplicate in a list with one planted"

def test_find_duplicates_on_clean_list():
    sample = [
        Transaction("2026-08-01", "Groceries", -50.0, "Food"),
        Transaction("2026-08-02", "Salary", 1000.0, "Salary"),
    ]
    duplicates = find_duplicates(sample)
    assert duplicates == [], "a clean list should have no duplicates"

def test_category_totals():
    sample = [
        Transaction("2026-08-01", "Groceries", -50.0, "Food"),
        Transaction("2026-08-02", "Takeout", -20.0, "Food"),
        Transaction("2026-08-03", "Salary", 1000.0, "Salary"),
    ]
    totals = category_totals(sample)
    assert totals["Food"] == -70.0, "Food category total is wrong"
    assert totals["Salary"] == 1000.0, "Salary category total is wrong"

def test_find_inconsistent_transactions():
    consistent_expense = Transaction("2026-08-01", "Groceries", -50.0, "Food")
    consistent_income = Transaction("2026-08-02", "Salary", 1000.0, "Salary")
    mismatched = Transaction("2026-08-03", "Freelance Payment", -300.0, "Freelance")
    unknown_category = Transaction("2026-08-04", "Mystery", -10.0, "Miscellaneous")
 
    flagged = find_inconsistent_transactions([consistent_expense, consistent_income, mismatched, unknown_category])
 
    assert consistent_expense not in flagged, "a negative Food amount is normal and should not be flagged"
    assert consistent_income not in flagged, "a positive Salary amount is normal and should not be flagged"
    assert mismatched in flagged, "a negative amount tagged as Freelance (income) should be flagged"
    assert unknown_category not in flagged, "an unrecognized category should not be flagged either way"

TESTS = [
    test_valid_row_parses_correctly,
    test_is_income,
    test_transaction_count_increments,
    test_recurring_transaction_override,
    test_normalize_date_validates_real_dates,
    test_loader_parses_valid_row,
    test_loader_normalizes_slash_dates,
    test_loader_rejects_junk_and_missing_fields,
    test_loader_rejects_non_numeric_amount,
    test_loader_rejects_invalid_calendar_date,
    test_loader_rejects_non_finite_amount,
    test_loader_rejects_empty_field,
    test_loader_handles_missing_file,
    test_loader_handles_empty_file,
    test_running_balance_sequence,
    test_make_flagger,
    test_find_duplicates_detects_planted_duplicate,
    test_find_duplicates_on_clean_list,
    test_category_totals,
    test_find_inconsistent_transactions,
]

def run_all_tests():
    for test in TESTS:
        test()
        print(f"  passed: {test.__name__}")
    print("\nAll tests passed.")

if __name__ == "__main__":
    run_all_tests()