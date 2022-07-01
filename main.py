from fastapi import FastAPI, HTTPException, status
from sqlmodel import create_engine, SQLModel, Session, select

from schemas import (
    Coffee,
    CoffeeOutput,
    CoffeeInput,
    ReviewInput,
    ReviewOutput,
)

app = FastAPI(title="PyCoffee")

engine = create_engine(
    "sqlite:///coffee.db", connect_args={"check_same_thread": False}, echo=True
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI"}


@app.get("/api/coffee")
def coffee_list(price: int | None = None, status: str | None = None) -> list:
    with Session(engine) as session:
        query = select(Coffee)
        if price:
            #query = [c for c in result if c.price >= price]
            query = query.where(Coffee.price >= price)

        if status:
            query = query.where(Coffee.status == price)
        return session.exec(query).all()


@app.get("/api/coffee/{id}")
def coffee_by_id(id: int) -> dict:
    result = [c for c in coffee_db if c.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No coffee with id: {id}"
        )


@app.post("/api/coffee", response_model=Coffee)
def add_coffee(coffee: CoffeeInput) -> Coffee:
    with Session(engine) as session:
        new_coffee = Coffee.from_orm(coffee)
        session.add(new_coffee)
        session.commit()
        session.refresh(new_coffee)
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
def add_review(coffee_id: int, reviews: ReviewInput) -> ReviewOutput:
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
