from fastapi import APIRouter
from app.api.v1.endpoints import auth,users,components, build, orders, guarantees




api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(components.router, prefix="/components", tags=["components"])
api_router.include_router(build.router, prefix="/build", tags=["components"])
api_router.include_router(orders.router, prefix="/orders",tags=["orders"])
api_router.include_router(guarantees.router, prefix="/guarantees",tags=["guarantees"])
