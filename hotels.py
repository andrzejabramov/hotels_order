from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH
# from fastapi_pagination import add_pagination, Page
# from fastapi_pagination.async_paginator import paginate


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    "/",
    summary="Получение списка отелей с применением фильтра",
    description="Либо получаем все отели, если не устанавливаем параметры, либо отдельно взятые",
)
def get_hotels(
    id: int | None= Query(None, description="Идентификатор Отеля"),
    title: str | None = Query(None, description="Название Отеля"),
    page: int | None = Query(1, description="Выберите страницу данных"),
    per_page: int | None = Query(3, description="Выберите количество отображаемых на странице строк")
):
    if all([not id, not title]):
        if page and per_page:
            start = (page - 1) * per_page
            end = start + per_page
            hotels_ = hotels[start:end]
            return hotels_
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

@router.post(
    "/",
    summary="Добавление Отеля",
    description="Добавляем Отель",
)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "motel_u_more"
        }
    },
    "2":{
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай у фонтана",
            "name": "dubai_u_fontain"
        }
    }})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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


