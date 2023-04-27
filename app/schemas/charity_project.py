from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.config import FIELD_MAX_LENGTH, FIELD_MIN_LENGTH


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=FIELD_MIN_LENGTH, max_length=FIELD_MAX_LENGTH
    )
    description: Optional[str] = Field(
        None, min_length=FIELD_MIN_LENGTH
    )
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ..., min_length=FIELD_MIN_LENGTH, max_length=FIELD_MAX_LENGTH
    )
    description: str = Field(
        ..., min_length=FIELD_MIN_LENGTH
    )
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    close_date: Optional[datetime]
    create_date: datetime
    fully_invested: bool
    id: int
    invested_amount: int

    class Config:
        orm_mode = True
