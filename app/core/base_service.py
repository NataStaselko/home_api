from typing import Type, TypeVar, Generic, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        """
        Базовый сервис для работы с моделью базы данных.

        :param model: SQLAlchemy модель, с которой работает сервис
        :param session: асинхронная сессия для работы с базой данных
        """
        self.model = model
        self.session = session

    async def get(self, obj_id: Any) -> Optional[T]:
        """
        Получить объект по ID.
        """
        query = select(self.model).filter(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, **kwargs) -> T:
        """
        Создать новый объект.
        """
        obj = self.model(**kwargs)
        self.session.add(obj)
        try:
            await self.session.commit()
            await self.session.refresh(obj)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return obj

    async def update(self, obj_id: Any, **kwargs) -> Optional[T]:
        """
        Обновить существующий объект.
        """
        obj = await self.get(obj_id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        try:
            await self.session.commit()
            await self.session.refresh(obj)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return obj

    async def delete(self, obj_id: Any) -> bool:
        """
        Удалить объект по ID.
        """
        obj = await self.get(obj_id)
        if not obj:
            return False
        try:
            await self.session.delete(obj)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return True

    async def list(self, offset: int = 0, limit: int = 10) -> list[T]:
        """
        Получить список объектов с пагинацией.
        """
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()