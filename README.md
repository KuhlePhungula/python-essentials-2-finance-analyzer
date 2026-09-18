# Personal Finance Transaction Analyzer
A menu-driven program that reads a messy bank-statement file, cleans and validates every row, tracks a running balance, breaks down spending by category, flags duplicate and unusual transactions, and writes a summary report - all built with the Python standard library.
**Author:** Kuhlekonke Phungula
**Cohort:** Data Science - Melsoft Academy
## Project structure
main.py           # menu loop, wires every module together
models.py         # Transaction class and a RecurringTransaction subclass
parser.py         # generates the sample file, loads & validates rows
analytics.py      # running balance (generator), flagger (closure),
                   # duplicate detection, outlier detection, category totals
reporting.py      # writes the monthly summary report and run log
tests.py          # self-tests - run standalone or via the menu
requirements.txt  # no third-party dependencies
data/             # generated at runtime (statement, report, log) - gitignore

## How to run
python main.py
