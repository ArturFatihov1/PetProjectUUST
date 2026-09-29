from fastapi import APIRouter, Body, Path, Query

from model import Todo

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:
    """Добавление задачи в список (валидация тела запроса моделью Todo)."""
    todo_list.append(todo)
    return {"message": "Задача успешно добавлена, Фатихов А.Д.!"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    """Получение всех задач."""
    return {"todos": todo_list}


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
        todo_id: int = Path(..., title="The ID of the todo to retrieve", gt=0),
) -> dict:
    """Получение одной задачи по параметру пути {todo_id}."""
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": "Задачи с таким ID не существует."}


@todo_router.get("/query")
async def query_route(query: str = Query(None, title="Фильтр по тексту задачи")) -> dict:
    """Параметр запроса ?query=... необязателен, поэтому по умолчанию None."""
    if query is None:
        return {"message": "Параметр query не передан, возвращаю все задачи.",
                "todos": todo_list}
    return {"query": query, "todos": [t for t in todo_list if query in t.item]}


@todo_router.put("/todo/{todo_id}")
async def update_todo(
        todo_id: int = Path(..., title="The ID of the todo to update", gt=0),
        todo: Todo = Body(..., title="Новое тело задачи"),
) -> dict:
    """Обновление существующей задачи (POST и UPDATE работают с телом запроса)."""
    for index, existing in enumerate(todo_list):
        if existing.id == todo_id:
            todo_list[index] = todo
            return {"message": "Задача успешно обновлена.", "todo": todo}
    return {"message": "Задачи с таким ID не существует."}


@todo_router.delete("/todo/{todo_id}")
async def delete_todo(
        todo_id: int = Path(..., title="The ID of the todo to delete", gt=0),
) -> dict:
    """Удаление задачи из списка."""
    for index, existing in enumerate(todo_list):
        if existing.id == todo_id:
            removed = todo_list.pop(index)
            return {"message": "Задача успешно удалена.", "todo": removed}
    return {"message": "Задачи с таким ID не существует."}
