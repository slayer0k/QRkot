from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import ProjectDonationBase


class Donation(ProjectDonationBase):
    __abstract__ = False
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return f'{self.__class__.name}: {self.id} - {self.user_id}'

    def __str__(self) -> str:
        return f'{self.__class__.name}: {self.id}'
