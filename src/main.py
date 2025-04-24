import sys
from pathlib import Path
from fastapi import FastAPI
import uvicorn
sys.path.append(str(Path(__file__).parent.parent))
# from fastapi.openapi.docs import get_swagger_ui_html
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_room
from cource_helpers.fastapi_load_test import router as router_speed

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_room)
app.include_router(router_speed)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)