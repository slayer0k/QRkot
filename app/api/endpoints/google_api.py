from typing import Dict, List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/', response_model=List[Dict],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service)
):
    '''Only for superusers'''
    projects = await charity_project_crud.get_projects_by_complection_rate(
        session
    )
    if not projects:
        return projects
    try:
        spreadsheet_id, grid = await spreadsheets_create(wrapper_service)
        await set_user_permissions(spreadsheet_id, wrapper_service)
        await spreadsheets_update_value(
            spreadsheet_id, projects, grid, wrapper_service
        )
    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f'{error}'
        )
    return projects
