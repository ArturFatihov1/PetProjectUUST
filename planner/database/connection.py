"""Подключение к нереляционной базе данных MongoDB через Beanie ODM."""

from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    """Настройки подключения, читаются из .env."""

    DATABASE_URL: Optional[str] = None

    async def initialize_database(self) -> None:
        """Создаёт асинхронный клиент MongoDB и регистрирует модели."""
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User],
        )

    class Config:
        env_file = ".env"


class Database:
    """Обёртка над Beanie-моделью для CRUD-операций."""

    def __init__(self, model) -> None:
        self.model = model

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc:
            return False
        body_data = body.model_dump(exclude_unset=True)
        body_data = {k: v for k, v in body_data.items() if v is not None}
        update_query = {"$set": {field: value for field, value in body_data.items()}}
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
