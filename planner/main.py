from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database.connection import conn
from routes.events import event_router
from routes.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создаёт таблицы SQLite при старте приложения."""
    conn()
    yield


app = FastAPI(
    title="Planner",
    description="Планировщик событий — ПЗ №7 «Подключение к реляционной базе данных»",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
