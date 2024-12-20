from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

def get_db_connection():
    connection = sqlite3.connect("db.sqlite")
    connection.row_factory = sqlite3.Row
    return connection

# Pydantic models
class Customer(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class Item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class Order(BaseModel):
    cust_id: Optional[int] = None
    notes: Optional[str] = None

# Endpoints for customers
@app.post("/customers")
def create_customer(customer: Customer):
    if not customer.name or not customer.phone:
        raise HTTPException(status_code=400, detail="Name and phone are required")
    connection = get_db_connection()
    connection.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    connection.commit()
    connection.close()
    return {"message": "Customer created successfully"}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    connection = get_db_connection()
    customer = connection.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    connection.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    connection = get_db_connection()
    connection.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    connection.commit()
    connection.close()
    return {"message": "Customer deleted successfully"}

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    connection = get_db_connection()
    existing_customer = connection.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not existing_customer:
        connection.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_name = customer.name if customer.name else existing_customer["name"]
    updated_phone = customer.phone if customer.phone else existing_customer["phone"]
    connection.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (updated_name, updated_phone, customer_id))
    connection.commit()
    connection.close()
    return {"message": "Customer updated successfully"}

# Endpoints for items
@app.post("/items")
def create_item(item: Item):
    if not item.name or item.price is None:
        raise HTTPException(status_code=400, detail="Name and price are required")
    connection = get_db_connection()
    connection.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    connection.commit()
    connection.close()
    return {"message": "Item created successfully"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    connection = get_db_connection()
    item = connection.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    connection.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    connection = get_db_connection()
    connection.execute("DELETE FROM items WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()
    return {"message": "Item deleted successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    connection = get_db_connection()
    existing_item = connection.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if not existing_item:
        connection.close()
        raise HTTPException(status_code=404, detail="Item not found")

    updated_name = item.name if item.name else existing_item["name"]
    updated_price = item.price if item.price is not None else existing_item["price"]
    connection.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (updated_name, updated_price, item_id))
    connection.commit()
    connection.close()
    return {"message": "Item updated successfully"}

# Endpoints for orders
@app.post("/orders")
def create_order(order: Order):
    if not order.cust_id:
        raise HTTPException(status_code=400, detail="Customer ID is required")
    connection = get_db_connection()
    connection.execute("INSERT INTO orders (notes, cust_id) VALUES (?, ?)", (order.notes, order.cust_id))
    connection.commit()
    connection.close()
    return {"message": "Order created successfully"}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    connection = get_db_connection()
    order = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    connection.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(order)

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    connection = get_db_connection()
    connection.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    connection.commit()
    connection.close()
    return {"message": "Order deleted successfully"}

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    connection = get_db_connection()
    existing_order = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not existing_order:
        connection.close()
        raise HTTPException(status_code=404, detail="Order not found")

    updated_notes = order.notes if order.notes else existing_order["notes"]
    connection.execute("UPDATE orders SET notes = ? WHERE id = ?", (updated_notes, order_id))
    connection.commit()
    connection.close()
    return {"message": "Order updated successfully"}
