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
