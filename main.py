from fastapi import FastAPI 
from datetime import datetime


app = FastAPI()

coffee_db = [
    {"id": 1, "name": "espresso","price": "49"},
    {"id": 2, "name": "americano","price": "59"},
    {"id": 3, "name": "latte","price": "59"},
    {"id": 4, "name": "mocha","price": "59"},
    {"id": 5, "name": "cappuccino","price": "59"},
    {"id": 6, "name": "cold brew","price": "69"},
    {"id": 7, "name": "green tea","price": "49"},
    {"id": 8, "name": "chocolate","price": "49"},
]

@app.get("/")
def welcome():
    return { "message": "Welcome to FastAPI"}

@app.get("/date")
def date():
    return { "date": datetime.now() }

@app.get("/api/coffee")
def coffee_list():
    return coffee_db
