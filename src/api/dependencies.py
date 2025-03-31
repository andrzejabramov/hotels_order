from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, description="Выберите страницу данных", ge=1)]
    per_page: Annotated[int | None, Query(None, description="Выберите количество отображаемых на странице строк", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParam, Depends()]