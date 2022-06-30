from fastapi import FastAPI, HTTPException, status


app = FastAPI()

coffee_db = [
    {"id": 1, "name": "espresso","price": 49, "status": "a"},
    {"id": 2, "name": "americano","price": 59, "status": "n"},
    {"id": 3, "name": "latte","price": 59, "status": "a"},
    {"id": 4, "name": "mocha","price": 59, "status": "a"},
    {"id": 5, "name": "cappuccino","price": 59, "status": "a"},
    {"id": 6, "name": "cold brew","price": 69, "status": "a"},
    {"id": 7, "name": "green tea","price": 49, "status": "n"},
    {"id": 8, "name": "chocolate","price": 49, "status": "n"},
]

@app.get("/")
def welcome():
    return { "message": "Welcome to FastAPI"}


@app.get("/api/coffee")
def coffee_list(price: int|None = None, status:str|None = None) -> list:
    result = coffee_db
    if price:
        result = [c for c in result if c["price"] >= price]

    if status:
        result = [c for c in result if c["status"] == status]

    return result


@app.get("/api/coffee/{id}")
def coffee_by_id(id: int) -> dict:
    result = [c for c in coffee_db if c["id"] == id] 
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id: {id}")
