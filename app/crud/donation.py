from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User


class CRUDDonations(CRUDBase):

    async def get_my_donations(
        self, user: User, session: AsyncSession
    ) -> List[Donation]:
        donations = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonations(Donation, CharityProject)
