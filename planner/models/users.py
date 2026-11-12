from typing import List, Optional

from pydantic import ConfigDict, EmailStr
from sqlmodel import JSON, Column, Field, SQLModel

from models.events import Event


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    events: List[dict] = Field(default_factory=list, sa_column=Column(JSON))


class NewUser(SQLModel):
    """Тело запроса POST /user/signup."""

    email: EmailStr
    password: str
    events: Optional[List[Event]] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "Stro0ng!",
                "events": [],
            }
        }
    )


class UserSignIn(SQLModel):
    """Тело запроса POST /user/signin."""

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "Stro0ng!",
            }
        }
    )
