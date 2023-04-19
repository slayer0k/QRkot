from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from app.core.config import (DESCRIPTION_ERROR, FIELD_MAX_LENGTH,
                             FIELD_MIN_LENGTH)
from app.models.abstract import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    __abstract__ = False
    name = Column(String(FIELD_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < FIELD_MIN_LENGTH:
            raise ValueError(DESCRIPTION_ERROR)
        return description

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.__class__.name} {self.id}'
