from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@router.get(
    "/",
    summary="Получение списка отелей с применением фильтра",
    description="Либо получаем все отели, если не устанавливаем параметры, либо отдельно взятые",
)
def get_hotels(
    id: int | None= Query(None, description="Идентификатор Отеля"),
    title: str | None = Query(None, description="Название Отеля"),
):
    if all([not id, not title]):
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

@router.post(
    "/",
    summary="Добавление Отеля",
    description="Добавляем Отель",
)
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
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
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body()
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"title": title, "name": name})
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление параметров",
    description="обновляются выборочно параметры"
)
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
):
    global hotels
    if all([not title, not name]):
        return {"status": "Необходимо заполнить хотя бы один параметр для изменения"}
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         if title:
    #             hotel["title"] = title
    #         if name:
    #             hotel["name"] = name
    return {"status": "Ok"}


