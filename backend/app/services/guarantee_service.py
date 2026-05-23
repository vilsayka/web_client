from fastapi import HTTPException
from app.repository.guarantee_repo import create_guarantee as repo_create_guarantee
from app.repository.order_repo_queries import get_order_by_id, get_order_components

def create_guarantee(conn, user_id: int, data: dict) -> dict:
    order_id = data["order_id"]
    comp_id = data["defective_component_id"]

    # 1. Заказ существует?
    order = get_order_by_id(conn, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Принадлежит ли заказ текущему пользователю?
    if order["id_customer"] != user_id:
        raise HTTPException(status_code=403, detail="You can only report on your own orders")

    # 3. Статус заказа должен быть "собрана"
    if order["status_order"] != "собрана":
        raise HTTPException(status_code=400, detail="Guarantee requests are only allowed for completed orders")

    # 4. Компонент должен быть в составе этого заказа
    components = get_order_components(conn, order_id)
    comp_ids = [c["id_component"] for c in components]
    if comp_id not in comp_ids:
        raise HTTPException(status_code=400, detail="Component does not belong to this order")

    # 5. Создаём обращение
    return repo_create_guarantee(conn, order_id, comp_id, data["problem_description"])