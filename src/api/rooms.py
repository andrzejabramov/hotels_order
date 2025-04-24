from fastapi import Query, Body, APIRouter

from src.repositories.rooms import RoomsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get(
    "/",
    summary="Получение списка номеров",
    description="Либо получаем все номера, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_rooms(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название Отеля"),
    location: str | None = Query(None, description="Местоположение Отеля")
):
    per_page = pagination.per_page or 5
#    logger.info(title, location, pagination.page, per_page)
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.get(
    "/{room_id}",
    summary="Получение одного Номера по id",
    description="Получаем Номер по одному обязательному параметру id",
)
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)

@router.post(
    "/",
    summary="Добавление Номера",
    description="Добавляем Номер",
)
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Ренессанс",
            "location": "Сочи, ул. Бирюзовая, 1"
        }
    },
    "2":{
        "summary": "Дубай",
        "value": {
            "title": "Шейхана",
            "location": "Дубай, ул. Шейха, 2"
        }
    }})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}

@router.delete(
    "/{room_id}",
    summary="Удаление выбранного Номера",
    description="Удаляем Номер"
)
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.put(
    "/{room_id}",
    summary="Обновление всех параметров выбранного Номера",
    description="Изменяем параметры только все пакетно"
)
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление параметров",
    description="обновляются выборочно параметры"
)
async def patch_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "Ok"}


