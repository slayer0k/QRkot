from typing import Dict, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.services import timedelta_to_format
from app.models import CharityProject, Donation


class CharityProjectCrud(CRUDBase):
    async def get_projects_by_complection_rate(
        self, session: AsyncSession
    ) -> List[Dict]:
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 1
            ).order_by(
                func.julianday(self.model.close_date) -
                func.julianday(self.model.create_date)
            )
        )
        return [
            dict(
                name=project.name,
                time_diff=timedelta_to_format(
                    project.close_date - project.create_date
                ),
                description=project.description,
            )
            for project in projects.scalars().all()
        ]


charity_project_crud = CharityProjectCrud(CharityProject, Donation)
