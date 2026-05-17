from fastapi import FastAPI
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware

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