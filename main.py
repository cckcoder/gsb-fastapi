from fastapi import FastAPI, HTTPException, status
from schemas import load_db

app = FastAPI()
coffee_db = load_db()


@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI"}


@app.get("/api/coffee")
def coffee_list(price: int | None = None, status: str | None = None) -> list:
    result = coffee_db
    if price:
        result = [c for c in result if c.price >= price]

    if status:
        result = [c for c in result if c.status == status]

    return result


@app.get("/api/coffee/{id}")
def coffee_by_id(id: int) -> dict:
    result = [c for c in coffee_db if c.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id: {id}"
        )
