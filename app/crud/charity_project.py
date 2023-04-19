from app.crud.base import CRUDBase
from app.models import CharityProject, Donation

charity_project_crud = CRUDBase(CharityProject, Donation)
