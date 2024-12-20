import sqlite3
import json

# Connect to the database
connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

# Drop tables if they exist (to avoid duplication errors)
cursor.execute("DROP TABLE IF EXISTS item_list")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS items")
cursor.execute("DROP TABLE IF EXISTS customers")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY,
    name CHAR(64) NOT NULL,
    phone CHAR(10) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY,
    name CHAR(64) NOT NULL,
    price REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cust_id INT NOT NULL,
    notes TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list(
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

# Open and read the JSON file
with open('example_orders.json', 'r') as file:
    data = json.load(file)

# Extract and insert customers
customers = {}
for order in data:
    name = order['name']
    phone = order['phone']
    customers[phone] = name

for phone, name in customers.items():
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

# Extract and insert items
items = {}
for order in data:
    for item in order['items']:
        name = item['name']
        price = item['price']
        items[name] = price

for name, price in items.items():
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))

# Extract and insert orders and item_list
for order in data:
    phone = order['phone']
    timestamp = order['timestamp']
    notes = order['notes']

    # Get customer ID
    res = cursor.execute("SELECT id FROM customers WHERE phone=?;", (phone,))
    cust_id = res.fetchone()[0]

    # Insert order
    cursor.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);", (timestamp, cust_id, notes))
    order_id = cursor.lastrowid

    # Add items in the item_list table
    for item in order['items']:
        name = item['name']
        res = cursor.execute("SELECT id FROM items WHERE name=?;", (name,))
        item_id = res.fetchone()[0]
        cursor.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item_id))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Database initialized and populated successfully!")
