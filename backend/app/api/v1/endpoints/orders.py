from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.services.order_service import change_order_status, create_order
from app.services.schemas.order import OrderCreate, OrderPublic, StatusUpdate
from dependency import get_current_user, get_db_master, get_db_slave
from app.services.order_service import get_order_details, take_order as take_order_service
from app.repository.order_repo_queries import (
    get_orders_by_customer,
    get_orders_by_importer,
    get_available_orders
)
router = APIRouter()

@router.post("/", response_model=OrderPublic, status_code=201)
def create_new_order(
    order_in: OrderCreate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    # Получаем id_customer через БД
    order = create_order(conn, current_user["user_id"], order_in.component_ids, order_in.warranty_period)
    # Возвращаем информацию о заказе с компонентами? Пока только базовые поля
    # Детали компонентов можно вернуть при запросе конкретного заказа.
    return OrderPublic(
        id_order=order["id_order"],
        id_customer=order["id_customer"],
        id_importer=order["id_importer"],
        status_order=order["status_order"],
        date_assembly=order.get("date_assembly"),
        warranty_period=order["warranty_period"],
        created_at=order["created_at"],
        total_price=None,  # потом вычислим
        components=None    # потом заполним
    )




@router.get("/", response_model=List[OrderPublic])
def list_orders(
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_slave)
):
    user_id = current_user["user_id"]
    role = current_user["role"]

    if role == "customer":
        orders = get_orders_by_customer(conn, user_id)
    elif role == "importer":
        orders = get_orders_by_importer(conn, user_id)
    else:
        orders = []  # admin

    result = []
    for o in orders:
        result.append(OrderPublic(
            id_order=o["id_order"],
            id_customer=o.get("id_customer", user_id),
            id_importer=o.get("id_importer"),
            customer_name=o.get("customer_name"),    # ✅ заполняем
            importer_name=o.get("importer_name"),    # ✅ заполняем
            status_order=o["status_order"],
            date_assembly=o.get("date_assembly"),
            warranty_period=o["warranty_period"],
            created_at=o["created_at"],
            total_price=None,
            components=None
        ))
    return result


@router.get("/available", response_model=List[OrderPublic])
def list_available_orders(
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_slave)
):
    if current_user["role"] != "importer":
        raise HTTPException(status_code=403, detail="Only importers can view available orders")
    orders = get_available_orders(conn)
    result = []
    for o in orders:
        result.append(OrderPublic(
            id_order=o["id_order"],
            id_customer=o["id_customer"],
            id_importer=None,
            customer_name=o["customer_name"],
            importer_name=None,
            status_order=o["status_order"],
            date_assembly=None,
            warranty_period=o["warranty_period"],
            created_at=o["created_at"],
            total_price=None,
            components=None
        ))
    return result


@router.get("/{order_id}", response_model=OrderPublic)
def read_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_slave)
):
    order = get_order_details(conn, order_id)
    # Проверка прав (оставь как есть)
    
    return OrderPublic(
        id_order=order["id_order"],
        id_customer=order["id_customer"],
        id_importer=order["id_importer"],
        customer_name=order.get("customer_name"),    # ✅
        importer_name=order.get("importer_name"),    # ✅
        status_order=order["status_order"],
        date_assembly=order.get("date_assembly"),
        warranty_period=order["warranty_period"],
        created_at=order["created_at"],
        total_price=order["total_price"],
        components=order["components"]
    )




@router.post("/{order_id}/take", response_model=OrderPublic)
def assign_importer(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    if current_user["role"] != "importer":
        raise HTTPException(status_code=403, detail="Only importers can take orders")
    order = take_order_service(conn, order_id, current_user["user_id"])
    return order

@router.patch("/{order_id}/status", response_model=OrderPublic)
def update_order_status_endpoint(
    order_id: int,
    status_update: StatusUpdate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    if current_user["role"] != "importer":
        raise HTTPException(status_code=403, detail="Only importers can change order status")
    return change_order_status(conn, order_id, current_user["user_id"], status_update.new_status)



