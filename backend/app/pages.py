from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.core.security import hash_password

pages_router = APIRouter()

@pages_router.get("/")
@pages_router.get("/main")
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



@pages_router.get("/main_user")
async def main_user():
    return FileResponse("../frontend/templates/main-user.html")


@pages_router.get("/personal_account")
async def personal_account():
    return FileResponse("../frontend/templates/personal_account.html")

@pages_router.get("/orders")
async def orders_page():
    return FileResponse("../frontend/templates/orders.html")

@pages_router.get("/order_detail")
async def order_detail_page():
    return FileResponse("../frontend/templates/order_detail.html")

@pages_router.get("/available_orders")
async def available_orders_page():
    return FileResponse("../frontend/templates/available_orders.html")

@pages_router.get("/my_guarantees")
async def my_guarantees_page():
    return FileResponse("../frontend/templates/my_guarantees.html")

@pages_router.get("/api/hash/{input_string}")
async def hash_string(input_string: str):
    hashed = hash_password(input_string)
    return {"original": input_string, "hash": hashed}


@pages_router.get("/dashboard")
async def dashboard_page():
    return FileResponse("../frontend/templates/dashboard.html")