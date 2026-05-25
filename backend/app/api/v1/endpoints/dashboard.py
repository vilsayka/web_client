from fastapi import APIRouter, Depends
from app.repository.order_repo import get_orders_stats  
from app.services.user_service import get_user_stats
from dependency import get_db_slave, require_admin  


router = APIRouter()

@router.get("/stats")
def dashboard_stats(conn = Depends(get_db_slave), _ = Depends(require_admin)):
    orders_by_status = get_orders_stats(conn)
    users_by_role = get_user_stats(conn)
    return {
        "orders_by_status": orders_by_status,
        "users_by_role": users_by_role
    }