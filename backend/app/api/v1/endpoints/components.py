from fastapi import APIRouter, Depends, Query
from app.services.component_service import get_components_by_category, get_all_components_grouped
from dependency import get_db_slave


router = APIRouter()

@router.get("/")
def list_components(category: str = Query(None), conn = Depends(get_db_slave)):
    if category:
        return get_components_by_category(conn, category)
    else:
        # Без параметра – возвращаем всё, сгруппированное для фронта
        return get_all_components_grouped(conn)