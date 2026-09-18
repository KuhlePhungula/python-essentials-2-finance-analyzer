# main menu

from parser import generate_sample_file, load_transactions, sample_file_path
from analytics import running_balance, find_duplicates, find_outliers, category_totals
from reporting import monthly_summary
import tests 

MENU = """
===== FINANCE TRANSACTION ANALYZER =====
1. Generate a messy sample statement file
2. Load & validate transactions (reject bad rows)
3. Show running balance (ledger)
4. Category breakdown (income vs expense by tag)
5. Detect duplicate transactions
6. Flag unusual transactions (statistical outliers)
7. Monthly summary report -> file
8. Run self-tests (tests.py)
9. Exit
"""

def main():
    transactions = []
    rejections = []
 
    while True:
        print(MENU)
        choice = input("Choose an option (1-9): ").strip()
 
        try:
            if choice == "1":
                generate_sample_file()
                print(f"Sample statement written to {sample_file_path}")
 
            elif choice == "2":
                transactions, rejections = load_transactions(sample_file_path)
                print(f"{len(transactions)} transactions loaded.")
                print(f"{len(rejections)} rows rejected:")
                for reason in rejections:
                    print(f"  - {reason}")
 
            elif choice == "3":
                if not transactions:
                    print("No transactions loaded yet - choose option 2 first.")
                else:
                    for transaction, balance in zip(transactions, running_balance(transactions)):
                        print(f"{transaction.formatted()}  ->  balance: {balance:.2f}")
 
            elif choice == "4":
                if not transactions:
                    print("No transactions loaded yet - choose option 2 first.")
                else:
                    for category, total in category_totals(transactions).items():
                        print(f"  {category}: {total:.2f}")
 
            elif choice == "5":
                if not transactions:
                    print("No transactions loaded yet - choose option 2 first.")
                else:
                    duplicates = find_duplicates(transactions)
                    print(f"{len(duplicates)} duplicate transaction(s) found:")
                    for transaction in duplicates:
                        print(f"  {transaction.formatted()}")
 
            elif choice == "6":
                if not transactions:
                    print("No transactions loaded yet - choose option 2 first.")
                else:
                    outliers = find_outliers(transactions)
                    print(f"{len(outliers)} unusual transaction(s) found (2+ standard deviations from the mean):")
                    for transaction in outliers:
                        print(f"  {transaction.formatted()}")
 
            elif choice == "7":
                if not transactions:
                    print("No transactions loaded yet - choose option 2 first.")
                else:
                    path = monthly_summary(transactions, rejections)
                    print(f"Report written to {path}")
 
            elif choice == "8":
                tests.run_all_tests()
 
            elif choice == "9":
                print("Goodbye!")
                break
 
            else:
                print("Please choose a number from 1 to 9.")
 
        except Exception as error:
            print(f"Something went wrong: {error}")
 
 
if __name__ == "__main__":
    main()