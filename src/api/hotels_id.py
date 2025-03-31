from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
# from fastapi_pagination import add_pagination, Page
# from fastapi_pagination.async_paginator import paginate


router = APIRouter(prefix="/hotels", tags=["Отели"])


# hotels = [
#     {"id": 1, "title": "Sochi", "name": "sochi"},
#     {"id": 2, "title": "Дубай", "name": "dubai"},
#     {"id": 3, "title": "Мальдивы", "name": "maldivi"},
#     {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
#     {"id": 5, "title": "Москва", "name": "moscow"},
#     {"id": 6, "title": "Казань", "name": "kazan"},
#     {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
# ]


@router.get(
    "/",
    summary="Получение списка отелей с применением фильтра",
    description="Либо получаем все отели, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_hotels(
    pagination: PaginationDep,
    id: int | None= Query(None, description="Идентификатор Отеля"),
    title: str | None = Query(None, description="Название Отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query= query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
    # if all([not id, not title]):
    #     if pagination.page and pagination.per_page:
    #         start = (pagination.page - 1) * pagination.per_page
    #         end = start + pagination.per_page
    #         hotels_ = hotels[start:end]
    #         return hotels_
        return hotels
    # return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

@router.post(
    "/",
    summary="Добавление Отеля",
    description="Добавляем Отель",
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1"
        }
    },
    "2":{
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай у фонтана",
            "location": "ул. Шейха, 2"
        }
    }})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}

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
        hotel["name"] = hotel_data.name
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         if title:
    #             hotel["title"] = title
    #         if hotel_data.name:
    #             hotel["name"] = name
    return {"status": "Ok"}


