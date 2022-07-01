from pathlib import Path

from sqlmodel import create_engine, Session

path = Path().resolve()
engine = create_engine(
    f"sqlite:///{path}/coffee.db", connect_args={"check_same_thread": False}, echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
