from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.services import investment, refreshing_object
from app.models import User


class CRUDBase:

    def __init__(self, model, second_model) -> None:
        self.model = model
        self.second_model = second_model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self, session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_opened(
        self, session: AsyncSession
    ):
        opened_objs = await session.execute(
            select(self.second_model).where(
                self.second_model.fully_invested == 0
            )
        )
        return opened_objs.scalars().all()

    async def create(
        self, obj_in,
        session: AsyncSession, user: User = None
    ):
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        await refreshing_object(db_obj, session)
        db_obj, sources = await investment(
            target=db_obj,
            sources=await self.get_opened(session),
        )
        session.add_all(sources)
        await refreshing_object(db_obj, session)
        return db_obj

    async def update(
            self, db_obj, obj_in, session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_none=True, exclude_unset=True)
        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
        await refreshing_object(db_obj, session)
        return db_obj

    async def remove(
            self, db_obj, session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_object_by_attribute(
        self,
        attr_name: str,
        atr_value: str,
        session: AsyncSession
    ):
        attr = getattr(self.model, attr_name)
        object = await session.execute(
            select(self.model).where(attr == atr_value)
        )
        return object.scalars().first()