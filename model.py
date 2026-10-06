from pydantic import BaseModel, ConfigDict


class Todo(BaseModel):
    """Модель задачи для тела запроса POST /todo (id + item)."""

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


from typing import List


class TodoItem(BaseModel):
    item: str

    class Config:
        schema_extra = {
            "example": {
                "item": "Read the next chapter of the book"
            }
        }


class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {"item": "Example schema 1!"},
                    {"item": "Example schema 2!"}
                ]
            }
        }
