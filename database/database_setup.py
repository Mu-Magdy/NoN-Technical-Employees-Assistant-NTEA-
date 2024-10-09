import sqlite3
import pandas as pd
import hashlib

# Step 1: Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("employee_data.db")
cursor = conn.cursor()

# Step 2: Create table schema (as per our single table structure)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone_number TEXT,
        department TEXT,
        position TEXT,
        hire_date TEXT,
        base_salary REAL,
        bonus REAL,
        currency TEXT,
        annual_leave_balance INTEGER,
        sick_leave_balance INTEGER,
        performance_rating REAL,
        review_period TEXT,
        last_review_date TEXT,
        password_hash TEXT,
        last_login TEXT
    )
"""
)

# Step 3: Load CSV data
df = pd.read_csv("employees.csv")

# Step 4: Insert data into the database
for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, department, position,
        hire_date, base_salary, bonus, currency, annual_leave_balance, sick_leave_balance, performance_rating,
        review_period, last_review_date, password_hash, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            row["employee_id"],
            row["first_name"],
            row["last_name"],
            row["email"],
            row["phone_number"],
            row["department"],
            row["position"],
            row["hire_date"],
            row["base_salary"],
            row["bonus"],
            row["currency"],
            row["annual_leave_balance"],
            row["sick_leave_balance"],
            row["performance_rating"],
            row["review_period"],
            row["last_review_date"],
            row["password_hash"],
            row["last_login"],
        ),
    )

print("Database setup complete and data inserted!")

# Step 5: Hash the default password ('password123')
default_password = "password123"
password_hash = hashlib.sha256(default_password.encode()).hexdigest()


# Update the password hash for all employees in the table
cursor.execute(
    """
    UPDATE employees
    SET password_hash = ?
""",
    (password_hash,),
)


# Step 5: Commit the transaction and close the connection
conn.commit()
conn.close()

print("All employees' password hashes have been updated.")
