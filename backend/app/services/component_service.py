from app.repository import component_repo
from fastapi import HTTPException

# маппинг русских категорий в английские title (как в твоих данных)
CATEGORY_MAP = {
    "Процессор": "Processor",
    "Материнская плата": "Motherboard",
    "Блок питания": "Power Supply",
    "Корпус": "Case",
    "Видеокарта": "Graphics Card",
    "Охлаждение процессора": "CPU Cooler",
    "Оперативная память": "RAM",
    "Накопители": "Storage"      
}

def get_component(conn, component_id: int):
    comp = component_repo.get_component(conn, component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")
    return comp

def get_components_by_category(conn, russian_category: str):
    eng_title = CATEGORY_MAP.get(russian_category)
    if not eng_title:
        raise HTTPException(status_code=400, detail="Unknown category")
    components = component_repo.get_components_by_title(conn, eng_title)
    # Преобразуем в формат для фронта
    result = []
    for c in components:
        name = f"{c['manufacturer']} {c['model']}"
        desc = f"{c['title']}"
        if c['specifications'].get('socket'):
            desc += f", сокет {c['specifications']['socket']}"
        if c['specifications'].get('cores'):
            desc += f", {c['specifications']['cores']} ядер"
        if c['specifications'].get('capacity_gb'):
            desc += f", {c['specifications']['capacity_gb']} ГБ"
        result.append({
            "id": c["id_component"],
            "name": name,
            "description": desc,
            "price": c["price_complete"]
        })
    return result


def get_all_components_grouped(conn):
    all_comps = component_repo.get_all_components(conn)
    grouped = {}
    for comp in all_comps:
        # Определяем русскую категорию по английскому title
        russian_cat = None
        for rus, eng in CATEGORY_MAP.items():
            if eng == comp["title"]:
                russian_cat = rus
                break
        if not russian_cat:
            russian_cat = comp["title"]  # fallback

        if russian_cat not in grouped:
            grouped[russian_cat] = []

        name = f"{comp['manufacturer']} {comp['model']}"
        desc = comp["title"]
        if comp['specifications'].get('socket'):
            desc += f", сокет {comp['specifications']['socket']}"
        if comp['specifications'].get('cores'):
            desc += f", {comp['specifications']['cores']} ядер"
        if comp['specifications'].get('capacity_gb'):
            desc += f", {comp['specifications']['capacity_gb']} ГБ"

        grouped[russian_cat].append({
            "id": comp["id_component"],
            "name": name,
            "description": desc,
            "price": comp["price_complete"]
        })

    result = [{"category": cat, "items": items} for cat, items in grouped.items()]
    return {"components": result}