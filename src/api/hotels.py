from fastapi import Query, Body, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей с применением фильтра",
    description="Либо получаем все отели, если не устанавливаем параметры, либо отдельно взятые",
)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название Отеля"),
    location: str | None = Query(None, description="Местоположение Отеля")
):
    per_page = pagination.per_page or 5
#    logger.info(title, location, pagination.page, per_page)
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get(
    "/{hotel_id}",
    summary="Получение одного Отеля по id",
    description="Получаем Отель по одному обязательному параметру id",
)
async def get_hotel(hotel_id: int, db: DBDep):
    ans = await db.hotels.get_one_or_none(id=hotel_id)
    res = "Такого отеля не существует" if not ans else ans
    return res

@router.post(
    "",
    summary="Добавление Отеля",
    description="Добавляем Отель",
)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}

@router.delete(
    "/{hotel_id}",
    summary="Удаление выбранного Отеля",
    description="Удаляем Отель"
)
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.put(
    "/{hotel_id}",
    summary="Обновление всех параметров выбранного Отеля",
    description="Изменяем параметры только все пакетно"
)
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление параметров",
    description="обновляются выборочно параметры"
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "Ok"}


