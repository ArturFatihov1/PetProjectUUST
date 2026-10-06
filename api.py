from fastapi import FastAPI

from todo import todo_router

app = FastAPI(
    title="PetProjectUUST",
    description="CRUD-приложение todo из ПЗ №4-1 «Модели ответов и обработка ошибок»",
    version="2.0.0",
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World, Фатихов А.Д.!"}


app.include_router(todo_router)
