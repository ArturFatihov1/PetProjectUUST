from typing import List, Optional

from pydantic import ConfigDict
from sqlmodel import JSON, Column, Field, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    location: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "Обсуждение книги по FastAPI. Приходите со своей копией!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            }
        }
    )


class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "location": "Hybrid",
            }
        }
    )
