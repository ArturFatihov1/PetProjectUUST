from fastapi import FastAPI

from todo import todo_router

app = FastAPI(
    title="PetProjectUUST",
    description="Приложение todo из ПЗ №4 «Маршрутизация в FastAPI»",
    version="1.0.0",
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World, Фатихов А.Д.!"}


app.include_router(todo_router)
