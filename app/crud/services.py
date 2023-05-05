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
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> Union[CharityProject, Donation]:
    required_funds = target.full_amount
    for source in sources:
        free_cash = source.full_amount - source.invested_amount
        if required_funds - free_cash < 0:
            target.fully_invested = True
            target.close_date = datetime.now()
            target.invested_amount = target.full_amount
            source.invested_amount += required_funds
            break
        source.fully_invested = True
        source.close_date = datetime.now()
        source.invested_amount = source.full_amount
        target.invested_amount += free_cash
        if target.full_amount == target.invested_amount:
            target.close_date = datetime.now()
            target.fully_invested = True
            target.invested_amount = target.full_amount
            break
    return target, sources


def timedelta_to_format(duration):
    FORMAT = '{} days, {}:{}:{}.{}'
    days, seconds = duration.days, duration.seconds
    microseconds = duration.microseconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return FORMAT.format(
        days, hours, minutes, seconds, microseconds
    )
