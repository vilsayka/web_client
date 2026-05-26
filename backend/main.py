from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from flask import jsonify
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.pages import pages_router

import os

static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")
templates_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "templates")

app = FastAPI(title="Vibecore API")

# Разрешаем запросы с фронтенда 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")
@app.get("/main")
async def root():
    return FileResponse("../frontend/templates/main.html")



app.mount("/static", StaticFiles(directory=static_dir), name="static")



app.mount("/pages", StaticFiles(directory=templates_dir), name="templates")

app.include_router(pages_router)

