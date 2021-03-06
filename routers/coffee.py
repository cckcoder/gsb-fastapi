from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from database.db_connect import get_session

from schemas import (
    Coffee,
    CoffeeInput,
    CoffeeOutput,
    Review,
    ReviewInput,
)
from utils.helper_exception import NotFoundException
from utils.oauth2 import access_user_token


router = APIRouter(
    prefix="/api/coffee", tags=["coffee"], dependencies=[Depends(access_user_token)]
)


@router.get("/")
def coffee_list(
    price: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_session),
) -> list:
    query = select(Coffee)
    if price:
        query = query.where(Coffee.price >= price)

    if status:
        query = query.where(Coffee.status == status)
    return db.exec(query).all()


@router.get("/{id}", response_model=CoffeeOutput)
def coffee_by_id(id: int, db: Session = Depends(get_session)) -> Coffee:
    coffee = db.get(Coffee, id)
    if coffee:
        return coffee
    else:
        raise NotFoundException()


@router.post("/", response_model=Coffee)
def add_coffee(coffee: CoffeeInput, db: Session = Depends(get_session)) -> Coffee:
    new_coffee = Coffee.from_orm(coffee)
    db.add(new_coffee)
    db.commit()
    db.refresh(new_coffee)
    return new_coffee


@router.put("/{id}", response_model=Coffee)
def update_coffee(
    id: int, new_coffee: CoffeeInput, db: Session = Depends(get_session)
) -> Coffee:
    coffee = db.get(Coffee, id)
    if coffee:
        coffee.name = new_coffee.name
        coffee.price = new_coffee.price
        coffee.status = new_coffee.status
        db.commit()
        return coffee
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"coffee id {id} not available",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_coffee(id: int, db: Session = Depends(get_session)) -> None:
    coffee = db.get(Coffee, id)
    if coffee:
        db.delete(coffee)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"coffee id {id} not available",
        )


@router.post("/{coffee_id}/reviews", response_model=Review)
def add_review(
    coffee_id: int, review: ReviewInput, db: Session = Depends(get_session)
) -> Review:
    coffee = db.get(Coffee, coffee_id)
    if coffee:
        new_review = Review.from_orm(review, update={"coffee_id": coffee_id})
        coffee.reviews.append(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"coffee id {id} not available",
        )
