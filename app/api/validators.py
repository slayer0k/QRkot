from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (CANT_REDUCE_AMOUNT, CANT_UPDATE_CLOSED_PROJECT,
                             EMPTY_REQUEST, PROJECT_DOESNT_EXISTS,
                             PROJECT_NAME_OCCUPIED, PROJECT_WAS_FUNDED)
from app.crud import charity_project_crud
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_exists(
    project_id: int,
    session: AsyncSession
):
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_DOESNT_EXISTS
        )
    return project


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession
):
    project = await charity_project_crud.get_object_by_attribute(
        'name', project_name, session
    )
    if project:
        raise HTTPException(
            status_code=400,
            detail=PROJECT_NAME_OCCUPIED
        )


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession
):
    project = await check_project_exists(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=PROJECT_WAS_FUNDED
        )
    return project


async def check_project_before_update(
    obj_in: CharityProjectUpdate,
    project_id: int,
    session: AsyncSession
):
    project = await check_project_exists(project_id, session)
    if not obj_in.dict(exclude_none=True):
        raise HTTPException(
            status_code=422,
            detail=EMPTY_REQUEST
        )
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail=CANT_UPDATE_CLOSED_PROJECT
        )
    if obj_in.full_amount:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail=CANT_REDUCE_AMOUNT
            )
    return project
