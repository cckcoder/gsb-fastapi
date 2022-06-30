import json 
from pydantic import BaseModel 


class Coffee(BaseModel):
    id: int
    name: str
    price: int
    status: str | None = "a"


def load_db() -> list[Coffee]:
    with open("coffee_db.json") as f:
        return [Coffee.parse_obj(obj) for obj in json.load(f)]


