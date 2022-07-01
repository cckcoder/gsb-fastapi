from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import SQLModel
from database.db_connect import engine
from routers import coffee


app = FastAPI(title="PyCoffee")
app.include_router(coffee.router)

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI"}
