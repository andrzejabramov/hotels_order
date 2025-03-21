from fastapi import FastAPI
import uvicorn
# from fastapi.openapi.docs import get_swagger_ui_html
from hotels import router as router_hotels
from cource_helpers.fastapi_load_test import router as router_speed


app = FastAPI()

app.include_router(router_hotels)
app.include_router(router_speed)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, workers=1)