from fastapi import FastAPI, Query, Body
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
    if all([not id, not title]):
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


@app.post("/hotels", tags=["Добавление Отеля"])
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}

@app.delete("/hotels/{hotel_id}", tags=["Удаление Отеля"])
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)