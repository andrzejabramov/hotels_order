from fastapi import APIRouter, HTTPException, Response, Request, Header
from fastapi.responses import JSONResponse

from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким from email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

# @router.get("/auth_only")
# async def auth_only(
#         request: Request,
#         authorization: str = Header(None)
# ):
#     # Попробуем получить токен из заголовка Authorization
#     if authorization:
#         # Обычно токен передается в формате "Bearer <token>"
#         token = authorization.split(' ')[1] if 'Bearer ' in authorization else authorization
#         return JSONResponse(content={"access_token": token})
#
#     # Если токен не найден в заголовках, проверим тело запроса
#     body = await request.json()
#     if 'access_token' in body:
#         return JSONResponse(content={"access_token": body['access_token']})
#
#     # Если токен не найден ни в заголовках, ни в теле запроса
#     raise HTTPException(status_code=400, detail="Access token not found in the request.")
@router.get("/auth_only")
async def auth_only(
        request: Request
):
    access_token = request.cookies.get("access_token", None)
    return access_token

