from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlmodel import SQLModel
from database.db_connect import engine
from routers import coffee, auth
from utils.helper_exception import NotFoundException, UnauthorizeException


app = FastAPI(title="PyCoffee")
app.include_router(coffee.router)
app.include_router(auth.router)

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


@app.exception_handler(NotFoundException)
async def excepition_404_handler(req: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Not found available coffee id"},
    )


@app.exception_handler(UnauthorizeException)
async def excepition_404_handler(req: Request, exc: UnauthorizeException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Invalid credential"},
    )


@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI"}
