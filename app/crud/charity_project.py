from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.services import timedelta_to_format
from app.models import CharityProject, Donation


class CharityProjectCrud(CRUDBase):
    async def get_projects_by_complection_rate(
        self, session: AsyncSession
    ) -> List[Dict]:
        projects = await session.execute(
            select(
                self.model.name,
                self.model.close_date,
                self.model.create_date,
                self.model.description
            ).where(
                self.model.fully_invested == 1
            )
        )
        results = [
            {
                'Название проекта': project.name,
                'Время сбора': project.close_date - project.create_date,
                'Описание проекта': project.description
            } for project in projects
        ]
        results = sorted(results, key=lambda x: x['Время сбора'])
        for obj in results:
            obj['Время сбора'] = timedelta_to_format(
                obj['Время сбора']
            )
        return results


charity_project_crud = CharityProjectCrud(CharityProject, Donation)
