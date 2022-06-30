from fastapi import FastAPI 
from datetime import datetime


app = FastAPI()

coffee_db = [
    {"id": 1, "name": "espresso","price": 49, "is_active": 1},
    {"id": 2, "name": "americano","price": 59, "is_active": 0},
    {"id": 3, "name": "latte","price": 59, "is_active": 1},
    {"id": 4, "name": "mocha","price": 59, "is_active": 1},
    {"id": 5, "name": "cappuccino","price": 59, "is_active": 1},
    {"id": 6, "name": "cold brew","price": 69, "is_active": 1},
    {"id": 7, "name": "green tea","price": 49, "is_active": 0},
    {"id": 8, "name": "chocolate","price": 49, "is_active": 0},
]

@app.get("/")
def welcome():
    return { "message": "Welcome to FastAPI"}

@app.get("/date")
def date():
    return { "date": datetime.now() }

@app.get("/api/coffee")
def coffee_list(price = None, is_active = None):
    result = coffee_db
    if price:
        result = [c for c in result if str(c["price"]) >= price]

    if is_active:
        result = [c for c in result if str(c["is_active"]) == is_active]

    return result
