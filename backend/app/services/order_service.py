# app/services/order_service.py
from typing import List

from app.repository import component_repo
from fastapi import HTTPException
from psycopg2 import errors
from app.repository.order_repo import create_order as repo_create_order

from app.repository.order_repo_queries import (
    get_orders_by_customer,
    get_order_by_id,
    get_order_components,
)
from app.repository.order_repo import add_components_to_order, assign_importer, update_order_status


def create_order(conn, id_customer: int, component_ids: list[int], warranty_period: int) -> dict:
    # Проверим, что все компоненты существуют
    for cid in component_ids:
        comp = component_repo.get_component(conn, cid)
        if not comp:
            raise HTTPException(status_code=404, detail=f"Component with id {cid} not found")
    try:
        order = repo_create_order(conn, id_customer, warranty_period)
        add_components_to_order(conn, order["id_order"], component_ids)
        # добавим компоненты в ответ (можно вернуть список)
        # пока без total_price, позже добавим
        return order
    except errors.UniqueViolation:  # на случай, если что-то дублируется (но вроде нечему)
        conn.rollback()
        raise HTTPException(status_code=409, detail="Order creation conflict")
    

def get_orders_for_user(conn, user_id: int, role: str) -> List[dict]:
    if role == "customer":
        return get_orders_by_customer(conn, user_id)
    elif role == "importer":
        # пока возвращаем пустой список или все заказы, где он назначен (позже добавим)
        return []
    elif role == "admin":
        return []  # админ видит все, но сделаем отдельный эндпоинт
    return []

def get_order_details(conn, order_id: int) -> dict:
    order = get_order_by_id(conn, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    components = get_order_components(conn, order_id)
    total_price = sum(c["price"] * c["quantity"] for c in components)
    order["components"] = components
    order["total_price"] = total_price
    return order


def take_order(conn, order_id: int, importer_id: int) -> dict:
    success = assign_importer(conn, order_id, importer_id)
    if not success:
        raise HTTPException(status_code=409, detail="Order is no longer available")
    return get_order_details(conn, order_id)


ALLOWED_TRANSITIONS = {
    'ожидает сборщика': ['на сборке'],
    'на сборке': ['собрана'],
    'собрана': [] 
}

def change_order_status(conn, order_id: int, importer_id: int, new_status: str) -> dict:
    order = get_order_by_id(conn, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["id_importer"] != importer_id:
        raise HTTPException(status_code=403, detail="Not your order")
    allowed = ALLOWED_TRANSITIONS.get(order["status_order"], [])
    if new_status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid status transition")
    success = update_order_status(conn, order_id, new_status, importer_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update status")
    return get_order_details(conn, order_id)