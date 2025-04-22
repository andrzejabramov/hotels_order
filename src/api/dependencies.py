from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated

from src.services.auth import AuthService


class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, description="Выберите страницу данных", ge=1)]
    per_page: Annotated[int | None, Query(None, description="Выберите количество отображаемых на странице строк", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParam, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]