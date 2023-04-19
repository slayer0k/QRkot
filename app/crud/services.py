from datetime import datetime
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def refreshing_object(
    object: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    session.add(object)
    await session.commit()
    await session.refresh(object)
    return object


async def investment(
    created_obj: Union[CharityProject, Donation],
    target_objs: List[Union[CharityProject, Donation]],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    index = 0
    required_funds = created_obj.full_amount
    while created_obj.fully_invested is False and index < len(target_objs):
        target_obj = target_objs[index]
        free_cash = target_obj.full_amount - target_obj.invested_amount
        if required_funds - free_cash < 0:
            created_obj.fully_invested = True
            created_obj.close_date = datetime.now()
            created_obj.invested_amount = created_obj.full_amount
            target_obj.invested_amount += required_funds
            session.add(target_obj)
        else:
            index += 1
            target_obj.fully_invested = True
            target_obj.close_date = datetime.now()
            target_obj.invested_amount = target_obj.full_amount
            created_obj.invested_amount += free_cash
            session.add(target_obj)
            if created_obj.full_amount == created_obj.invested_amount:
                created_obj.close_date = datetime.now()
                created_obj.fully_invested = True
                created_obj.invested_amount = created_obj.full_amount
    return created_obj
