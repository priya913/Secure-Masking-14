
import sqlite3
import csv

# 1. Create an in-memory SQLite database
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# 2. Create customer sales table
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    sales_amount REAL
)
""")

# 3. Insert simulated customer data
customers = [
    (1, "Arun Kumar", "arun@gmail.com", "9876543210", 15000),
    (2, "Priya Sharma", "priya@gmail.com", "9876543211", 22000),
    (3, "Rahul Kumar", "rahul@gmail.com", "9876543212", 18000),
    (4, "Divya Raj", "divya@gmail.com", "9876543213", 25000),
    (5, "Karthik S", "karthik@gmail.com", "9876543214", 30000)
]

cursor.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
    customers
)
connection.commit()


# 4. Secure parameterized SQL query
def secure_query(customer_id):
    query = """
    SELECT customer_id, customer_name, email,
           phone, sales_amount
    FROM customers
    WHERE customer_id = ?
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()


# 5. Email masking
def mask_email(email):
    username, domain = email.split("@")
    return username[0] + "****@" + domain


# 6. Phone masking
def mask_phone(phone):
    return "XXXXXX" + phone[-4:]


# 7. Display original data
print("\n===== ORIGINAL CUSTOMER DATA =====")

original_data = cursor.execute(
    "SELECT * FROM customers"
).fetchall()

for row in original_data:
    print(row)


# 8. Display masked data
print("\n===== MASKED CUSTOMER DATA =====")

masked_data = []

for row in original_data:
    masked_row = (
        row[0],
        row[1],
        mask_email(row[2]),
        mask_phone(row[3]),
        row[4]
    )

    masked_data.append(masked_row)
    print(masked_row)


# 9. Test parameterized query
print("\n===== SECURE QUERY TEST =====")

result = secure_query("1")
print("Customer ID 1:", result)

# SQL injection test
attack = secure_query("1 OR 1=1")
print("SQL injection test:", attack)


# 10. Export masked data to CSV
with open("masked_sales.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "customer_id",
        "customer_name",
        "email",
        "phone",
        "sales_amount"
    ])

    writer.writerows(masked_data)

print("\nMasked data exported to masked_sales.csv")

connection.close()
