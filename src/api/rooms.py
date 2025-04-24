from fastapi import Query, Body, APIRouter

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение списка номеров Отеля",
    description="Либо получаем все номера, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_rooms(hotel_id: int):
#    logger.info(title, location, pagination.page, per_page)
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение одного Номера по id",
    description="Получаем Номер по одному обязательному параметру id",
)
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        ans = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        res = "Такого номера не существует" if not ans else ans
        return res

@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление Номера",
    description="Добавляем Номер",
)
async def create_room(hotel_id: str, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}

@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление выбранного Номера",
    description="Удаляем Номер"
)
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        ans = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if not ans:
            return "Такого номера не существует"
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех параметров выбранного Номера",
    description="Изменяем параметры только все пакетно"
)
async def edit_room(hotel_id, room_id: int, room_data: RoomAddRequest):
    async with async_session_maker() as session:
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление параметров",
    description="обновляются выборочно параметры"
)
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    async with async_session_maker() as session:
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "Ok"}


