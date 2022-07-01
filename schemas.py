from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext
from pydantic import BaseModel


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


pwd_context = CryptContext(schemes=["bcrypt"])


class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    username: str = Field(
        sa_column=Column("username", VARCHAR, unique=True, index=True)
    )
    password_hash: str = ""

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Token(BaseModel):
    access_token: str
    token_type: str
