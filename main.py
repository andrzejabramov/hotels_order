from fastapi import FastAPI, Query
import uvicorn
# from fastapi.openapi.docs import get_swagger_ui_html


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"},
]


@app.get("/hotels", tags=["Список Отелей"])
def get_hotels(
        id: int | None= Query(None, description="Идентификатор Отеля"),
        title: str | None = Query(None, description="Название Отеля"),
):
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)