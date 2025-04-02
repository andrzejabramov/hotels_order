# Заказ отелей

## I. Виртуальное окружение
### В venv по совету Артема используем Python3.11
### У меня почему-то не получилось установить python3.11 сторокой:
```commandline
python3.11 -m venv .venv
```
Потому что, не был предустановлен 3.11 (есть 3.9, 3.10, 3.12)
Для установки 3.11 использовал pyvenv:
```commandline
pyvenv install 3.11.11
```
После установки проверяем:
```
pyvenv install --list
```
Заходим в папку проекта hotels_order и делаем 3.11 локальной для проекта:
```commandline
pyvenv local 3.11.11 
```
Появился файл .python-version
Теперь можно создать виртуальное окружение командой:
```
python3 -m venv .venv
```
Все, подтянулась 3.11.11

## Варианты запуска приложения Fastapi
#### 1.  
```
fastapi dev main.py
```
#### 2. 
```commandline
uvicorn main:app --reload
```
### 3.
```commandline
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```
```commandline
python3 main.py
```

## Ручка получение отелей
```commandline
@app.get("/hotels", tags=["Список Отелей"])
def get_hotels(
        id: int | None= Query(None, description="Идентификатор Отеля"),
        title: str | None = Query(None, description="Название Отеля"),
):
    if all([not id, not title]):
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

```
#### Если параметры в документации не указаны: выводится список всех отелей, если же указаны либо id либо наименование,то по этому параметру фильтруется список

## Ручка добавление отеля (post): 
```commandline
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
```
embed=True выводит в броузере в json

# Настройка БД для работы в кодировке UTF-8

```commandline
SET client_encoding = 'UTF8';
UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';
```

Каждую строку кода выполнять отдельно (если в клиенте: бобер, навикат) в новом окне SQL запроса 
