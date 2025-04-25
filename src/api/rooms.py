from fastapi import Body, APIRouter

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение списка номеров Отеля",
    description="Либо получаем все номера, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_rooms(hotel_id: int, db: DBDep):
#    logger.info(title, location, pagination.page, per_page)
    return await db.rooms.get_filtered(hotel_id=hotel_id)

@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение одного Номера по id",
    description="Получаем Номер по одному обязательному параметру id",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    #res = "Такого номера не существует" if not ans else ans
    #return res

@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление Номера",
    description="Добавляем Номер",
)
async def create_room(
        hotel_id: str,
        db: DBDep,
        room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление выбранного Номера",
    description="Удаляем Номер"
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    # ans = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
    # if not ans:
    #     return "Такого номера не существует"
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех параметров выбранного Номера",
    description="Изменяем параметры только все пакетно"
)
async def edit_room(
        hotel_id,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
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
        db: DBDep,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"status": "Ok"}


