from fastapi import FastAPI, HTTPException, status
from schemas import CoffeeOutput, CoffeeInput, ReviewInput, ReviewOutput, load_db, save_db

app = FastAPI(title="PyCoffee")
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


@app.post("/api/coffee", response_model=CoffeeOutput)
def add_coffee(coffee: CoffeeInput) -> CoffeeOutput:
    id = len(coffee_db) + 1
    new_coffee = CoffeeOutput(
        id=id, name=coffee.name, price=coffee.price, status=coffee.status
    )

    coffee_db.append(new_coffee)
    save_db(coffee_db)
    return new_coffee


@app.put("/api/coffee/{id}", response_model=CoffeeOutput)
def update_coffee(id: int, new_coffee: CoffeeInput) -> CoffeeOutput:
    match = [c for c in coffee_db if c.id == id]
    if match:
        coffee = match[0]
        coffee.name = new_coffee.name
        coffee.price = new_coffee.price
        coffee.status = new_coffee.status
        save_db(coffee_db)
        return coffee
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id={id}"
        )


@app.delete("/api/coffee/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_coffee(id: int) -> None:
    match = [c for c in coffee_db if c.id == id]
    if match:
        coffee = match[0]
        coffee_db.remove(coffee)
        save_db(coffee_db)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id={id}"
        )


@app.post("/api/coffee/{coffee_id}/reviews", response_model=ReviewOutput)
def add_review(coffee_id:int, reviews: ReviewInput) -> ReviewOutput:
    match = [c for c in coffee_db if c.id == coffee_id]
    if match:
        coffee = match[0]
        new_review = ReviewOutput(id=len(coffee.reviews) + 1, **reviews.dict())
        coffee.reviews.append(new_review)
        save_db(coffee_db)
        return new_review
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id={id}"
        )
