from typing import List

from fastapi import HTTPException
from app.repository.guarantee_repo import create_guarantee as repo_create_guarantee, get_service_guarantees_by_user_id
from app.repository.order_repo_queries import get_order_by_id, get_order_components

def create_guarantee(conn, user_id: int, data: dict) -> dict:
    order_id = data["order_id"]
    comp_id = data["defective_component_id"]

    order = get_order_by_id(conn, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["id_customer"] != user_id:
        raise HTTPException(status_code=403, detail="You can only report on your own orders")

    if order["status_order"] != "собрана":
        raise HTTPException(status_code=400, detail="Guarantee requests are only allowed for completed orders")
    
    components = get_order_components(conn, order_id)
    comp_ids = [c["id_component"] for c in components]
    if comp_id not in comp_ids:
        raise HTTPException(status_code=400, detail="Component does not belong to this order")
    

    return repo_create_guarantee(conn, order_id, comp_id, data["problem_description"])


def get_service_guarantees_for_user(conn, user_id: int) -> List[dict]:
    return get_service_guarantees_by_user_id(conn, user_id)