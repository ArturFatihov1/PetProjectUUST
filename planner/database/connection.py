"""Подключение приложения-планировщика к базе данных SQLite."""

from sqlmodel import Session, SQLModel, create_engine

from models.events import Event
from models.users import User

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}

engine = create_engine(
    database_connection_string,
    echo=True,
    connect_args=connect_args,
)


def conn() -> None:
    """Создаёт файл базы данных и таблицы event и user."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Отдаёт сессию SQLModel и закрывает её после запроса."""
    with Session(engine) as session:
        yield session
