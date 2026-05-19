from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.pages import pages_router


app = FastAPI(title="Vibecore API")

# Разрешаем запросы с фронтенда (потом укажешь точный адрес)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем основной роутер (все эндпоинты внутри)
app.include_router(api_router, prefix="/api/v1")
@app.get("/main")
async def root():
    return FileResponse("../frontend/templates/main.html")

app.include_router(api_router, prefix="/api/v1")


app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


app.mount("/pages", StaticFiles(directory="../frontend/templates", html=True), name="templates")

app.include_router(pages_router)