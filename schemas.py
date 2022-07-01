from sqlmodel import SQLModel, Field, Relationship


class ReviewInput(SQLModel):
    star: int
    comment: str


class ReviewOutput(ReviewInput):
    id: int


class Review(ReviewInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    coffee_id: int = Field(foreign_key="coffee.id")
    coffee: "Coffee" = Relationship(back_populates="reviews")


class CoffeeInput(SQLModel):
    name: str
    price: int
    status: str | None = "a"

    class Config:
        schema_extra = {
            "example": {
                "name": "espresso",
                "price": 49,
                "status": "a",
            }
        }


class Coffee(CoffeeInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    reviews: list[Review] = Relationship(back_populates="coffee")


class CoffeeOutput(CoffeeInput):
    id: int
    reviews: list[ReviewOutput] = []


# def load_db() -> list[CoffeeOutput]:
# with open("coffee_db.json") as f:
# return [CoffeeOutput.parse_obj(obj) for obj in json.load(f)]
#
#
# def save_db(coffee_db: list[CoffeeOutput]):
# with open("coffee_db.json", "w") as f:
# json.dump([coffee.dict() for coffee in coffee_db], f, indent=4)
