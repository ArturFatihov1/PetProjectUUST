"""Подключение приложения-планировщика к базе данных SQLite."""

from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

from models.events import Event
from models.users import User

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False, "timeout": 30}

engine = create_engine(
    database_connection_string,
    echo=True,
    connect_args=connect_args,
)


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
    """Включает WAL и ожидание блокировки вместо ошибки database is locked.

    В обычном журнальном режиме SQLite читатель и писатель блокируют друг
    друга (например, сервер и открытая база в DB Navigator), из-за чего
    запросы падают с sqlite3.OperationalError. WAL разводит их, а busy_timeout
    заставляет ждать освобождения блокировки вместо мгновенной ошибки.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=30000")
    cursor.close()


def conn() -> None:
    """Создаёт файл базы данных и таблицы event и user."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Отдаёт сессию SQLModel и закрывает её после запроса."""
    with Session(engine) as session:
        yield session
