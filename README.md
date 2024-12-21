Dosa Restaurant API:

We will manage backend for a dosa restaurant. It allows you to easily handle customers, menu items, and orders. Built using FastAPI and SQLite, it’s fast, reliable, and easy to use.

Features:

Manage Customers: Add, update, view, and delete customer information.
Manage Items: Add, update, view, and delete item information.
Manage Orders: Add, update, view, and delete order information.

Setting Up the Project:

Install Required Libraries: pip install fastapi uvicorn
Set Up the Database: Run the script to create and populate the database; python init_db.py
Set up the main.py file and run the file

Start the API Server:

Use this command to start the server: python -m uvicorn main:app --reload
Once the server is running, open the browser:
Swagger Docs: http://127.0.0.1:8000/docs

Testing the API:

Open your browser and navigate to: http://127.0.0.1:8000/docs
You’ll find an easy-to-use interface to test all the API endpoints.
