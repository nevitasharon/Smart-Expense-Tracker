
import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from database import (
    create_table,
    add_expense,
    get_expenses,
    create_budget_table,
    set_budget,
    get_budget
)

# Configure the application
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Create database table
create_table()
create_budget_table()

# Application heading
st.title("💰 Smart Expense Tracker")
st.write("Manage your money. Understand your spending.")

st.divider()

# Fetch expenses from SQLite
expenses = get_expenses()

# Convert database records into a DataFrame
df = pd.DataFrame(
    expenses,
    columns=["ID", "Amount", "Category", "Description", "Date"]
)

# Dashboard metrics
total = df["Amount"].sum() if not df.empty else 0
transaction_count = len(df)

col1, col2 = st.columns(2)

col1.metric("Total Expenses", f"₹{total:,.2f}")
col2.metric("Number of Transactions", transaction_count)

st.divider()

# Add expense section
st.subheader("➕ Add a New Expense")

with st.form("expense_form"):

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Other"
        ]
    )

    description = st.text_input("Description")

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        add_expense(
            amount,
            category,
            description,
            expense_date
        )

        st.success("Expense saved successfully!")

        st.rerun()

# Transaction history
st.divider()
st.subheader("📋 Transaction History")

# Refresh database records
expenses = get_expenses()

df = pd.DataFrame(
    expenses,
    columns=["ID", "Amount", "Category", "Description", "Date"]
)

if not df.empty:

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

else:
    st.info("No expenses recorded yet.")


# Expense Analytics
st.divider()
st.header("📊 Expense Analytics")

if not df.empty:

    # Category-wise spending
    st.subheader("Spending by Category")

    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Expense Distribution")

    st.pyplot(fig)
    plt.close(fig)

    # Monthly spending analysis
    st.subheader("Monthly Spending")

    df["Date"] = pd.to_datetime(df["Date"])

    monthly_totals = df.groupby(
        df["Date"].dt.to_period("M")
    )["Amount"].sum()

    fig, ax = plt.subplots()

    ax.bar(
        monthly_totals.index.astype(str),
        monthly_totals.values
    )

    ax.set_title("Monthly Expenses")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")

    plt.xticks(rotation=45)

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Add expenses to see your analytics.")



# Monthly Budget Management
st.divider()
st.header("💰 Monthly Budget")

current_month = date.today().strftime("%Y-%m")

# Get saved budget
saved_budget = get_budget(current_month)

# Calculate current month's expenses
if not df.empty:
    dates = pd.to_datetime(df["Date"])

    monthly_expenses = df.loc[
        dates.dt.strftime("%Y-%m") == current_month,
        "Amount"
    ].sum()
else:
    monthly_expenses = 0

# Budget input
with st.form("budget_form"):

    budget = st.number_input(
        "Set your monthly budget (₹)",
        min_value=0.0,
        value=float(saved_budget),
        step=500.0
    )

    budget_submitted = st.form_submit_button("Save Budget")

    if budget_submitted:
        set_budget(current_month, budget)
        st.success("Monthly budget saved!")
        st.rerun()

# Display budget information
if saved_budget > 0:

    remaining = saved_budget - monthly_expenses

    st.metric(
        "Monthly Budget",
        f"₹{saved_budget:,.2f}"
    )

    st.metric(
        "Amount Spent",
        f"₹{monthly_expenses:,.2f}"
    )

    st.metric(
        "Remaining Budget",
        f"₹{remaining:,.2f}"
    )

    progress = min(monthly_expenses / saved_budget, 1.0)

    st.progress(progress)

    if monthly_expenses > saved_budget:
        st.error("⚠️ You have exceeded your monthly budget!")

    elif monthly_expenses >= saved_budget * 0.8:
        st.warning("⚠️ You have used 80% or more of your budget!")

    else:
        st.success("You're within your monthly budget!")

# Export expenses
st.divider()
st.header("📥 Download Expense Report")

if not df.empty:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:
    st.info("Add expenses before downloading a report.")