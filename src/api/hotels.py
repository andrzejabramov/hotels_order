from docutils.nodes import title
from fastapi import Query, Body, APIRouter
from sqlalchemy import insert
from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from loguru import logger

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/",
    summary="Получение списка отелей с применением фильтра",
    description="Либо получаем все отели, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название Отеля"),
    location: str | None = Query(None, description="Местоположение Отеля")
):
    per_page = pagination.per_page or 5
#    logger.info(title, location, pagination.page, per_page)
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.post(
    "/",
    summary="Добавление Отеля",
    description="Добавляем Отель",
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        #add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        #await session.execute(add_hotel_stmt)
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "OK", "data": hotel}

@router.delete(
    "/{hotel_id}",
    summary="Удаление выбранного Отеля",
    description="Удаляем Отель"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.put(
    "/{hotel_id}",
    summary="Обновление всех параметров выбранного Отеля",
    description="Изменяем параметры только все пакетно"
)
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"title": hotel_data.title, "name": hotel_data.name})
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление параметров",
    description="обновляются выборочно параметры"
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    if all([not hotel_data.title, not hotel_data.name]):
        return {"status": "Необходимо заполнить хотя бы один параметр для изменения"}
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.namee
    return {"status": "Ok"}


