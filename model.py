"""Модели Pydantic для валидации тела запроса (ПЗ №4, раздел 1.3)."""

from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    """Вложенная модель: описание самой задачи с её статусом."""

    item: str
    status: str


class Todo(BaseModel):
    """Основная модель задачи.

    FastAPI использует аннотацию `todo: Todo` как схему тела запроса,
    поэтому в список попадут только поля id и item, а лишние поля
    будут отброшены, а отсутствующие — вызовут ошибку валидации 422.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "item": "Example schema!",
            }
        }
    )

    id: int
    item: str


class NestedTodo(BaseModel):
    """Пример вложенной модели (ПЗ №4, раздел 1.3.1)."""

    id: int
    item: Item
