
import sqlite3


# Connect to the database
def connect_db():
    conn = sqlite3.connect("expenses.db")
    return conn


# Create the expenses table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add a new expense
def add_expense(amount, category, description, expense_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, str(expense_date)))

    conn.commit()
    conn.close()


# Retrieve all expenses
def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")

    expenses = cursor.fetchall()

    conn.close()

    return expenses


# Create a table for monthly budgets
def create_budget_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            month TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Save or update a monthly budget
def set_budget(month, amount):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO budgets (month, amount)
        VALUES (?, ?)
    """, (month, amount))

    conn.commit()
    conn.close()


# Retrieve a monthly budget
def get_budget(month):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (month,)
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0
