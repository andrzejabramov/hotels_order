from fastapi import APIRouter
from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except Exception as e:
            raise (f"ошибка {e}")
        else:
            return {"status": "OK"}