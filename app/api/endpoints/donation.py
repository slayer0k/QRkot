from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationGet,
                                  DonationSuperUserGet)

router = APIRouter()


@router.post(
    '/', response_model=DonationGet,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    sesion: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.create(donation, sesion, user)


@router.get(
    '/', response_model=List[DonationSuperUserGet],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my', response_model=List[DonationGet],
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_my_donations(
        user, session
    )
