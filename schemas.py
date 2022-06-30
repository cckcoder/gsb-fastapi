import json
from pydantic import BaseModel


class CoffeeInput(BaseModel):
    name: str
    price: int
    status: str | None = "a"


class CoffeeOutput(CoffeeInput):
    id: int


def load_db() -> list[CoffeeOutput]:
    with open("coffee_db.json") as f:
        return [CoffeeOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(coffee_db: list[CoffeeOutput]):
    with open("coffee_db.json", "w") as f:
        json.dump([coffee.dict() for coffee in coffee_db], f, indent=4)
