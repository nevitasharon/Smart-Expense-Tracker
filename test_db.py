from database import create_table, add_expense, get_expenses
from datetime import date

create_table()

add_expense(150, "Food", "Test Lunch", date.today())

expenses = get_expenses()

for expense in expenses:
    print(expense)