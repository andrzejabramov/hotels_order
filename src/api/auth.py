from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password
    )
    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким from email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"user": "logout"}


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
@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

