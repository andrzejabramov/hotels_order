from fastapi import Query, Body, APIRouter

from src.api.dependencies import PaginationDep, DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

#logger.add("/src/logs/logs.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    #получить цену номера
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    #создать схему данных BookingAdd
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    # добавить бронирование конкретному пользователю
    booking = await db.bookings.add(_booking_data)
    return {'status': 'ok', 'data': booking}