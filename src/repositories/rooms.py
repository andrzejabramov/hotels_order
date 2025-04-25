from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def get_one_or_none(self, **filter_by):
    #     parent = super().get_one_or_none
    #     if not parent:
    #         return "Такого номера не существует"
    #     return parent

