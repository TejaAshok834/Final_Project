import sqlite3

def fetch_customers():
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    connection.close()
    print("Customers Table Records:")
    for row in rows:
        print(row)

# Call the function to fetch and display records
fetch_customers()
