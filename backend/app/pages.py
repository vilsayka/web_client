from fastapi import APIRouter
from fastapi.responses import FileResponse

pages_router = APIRouter()

@pages_router.get("/")
@pages_router.get("/home")
async def home():
    return FileResponse("../frontend/templates/main.html")

@pages_router.get("/login")
async def login():
    return FileResponse("../frontend/templates/login.html")

@pages_router.get("/register")
async def register():
    return FileResponse("../frontend/templates/registration.html")


@pages_router.get("/pc_assembly")
async def pc_assembly():
    return FileResponse("../frontend/templates/create-pc.html")