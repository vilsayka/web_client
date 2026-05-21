# from psycopg2.extras import Json
# from typing import Optional, List


# def create_component(conn, data: dict) -> dict:
#     with conn.cursor() as cur:
#         cur.execute(
#             """INSERT INTO components (title, manifacturer, model, warranty_period, price_complete, quantity_accessories, specifications)
#             VALUES = """
#         )

import psycopg2
from psycopg2.extras import Json
from typing import Optional, List

def create_component(conn, data: dict) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO components (title, manufacturer, model, warranty_period, price_complete,
               quantity_accessories, specifications)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id_component, created_at, updated_at""",
            (data["title"], data["manufacturer"], data["model"],
             data.get("warranty_period", 0),
             data["price_complete"],
             data.get("quantity_accessories", 0),
             Json(data.get("specifications", {})))
        )
        row = cur.fetchone()
    conn.commit()
    return {
        "id_component": row[0],
        "created_at": row[1],
        "updated_at": row[2],
        **data
    }

def get_component(conn, component_id: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT id_component, title, manufacturer, model, warranty_period, price_complete,
               quantity_accessories, specifications, created_at, updated_at
               FROM components WHERE id_component = %s""",
            (component_id,))
        row = cur.fetchone()
        if row:
            return {
                "id_component": row[0],
                "title": row[1],
                "manufacturer": row[2],
                "model": row[3],
                "warranty_period": row[4],
                "price_complete": float(row[5]),
                "quantity_accessories": row[6],
                "specifications": row[7] if row[7] else {},
                "created_at": row[8],
                "updated_at": row[9]
            }
    return None

def get_components_by_title(conn, title: str) -> List[dict]:
    """Получить все компоненты с указанным title (например 'Processor')."""
    with conn.cursor() as cur:
        cur.execute(
            """SELECT id_component, title, manufacturer, model, warranty_period, price_complete,
               quantity_accessories, specifications, created_at, updated_at
               FROM components WHERE title = %s
               ORDER BY manufacturer, model""",
            (title,))
        rows = cur.fetchall()
        return [{
            "id_component": r[0],
            "title": r[1],
            "manufacturer": r[2],
            "model": r[3],
            "warranty_period": r[4],
            "price_complete": float(r[5]),
            "quantity_accessories": r[6],
            "specifications": r[7] if r[7] else {},
            "created_at": r[8],
            "updated_at": r[9]
        } for r in rows]
    

def get_all_components(conn) -> List[dict]:
    with conn.cursor() as cur:
        cur.execute("SELECT id_component, title, manufacturer, model, warranty_period, price_complete, quantity_accessories, specifications, created_at, updated_at FROM components")
        rows = cur.fetchall()
        return [{
            "id_component": r[0],
            "title": r[1],
            "manufacturer": r[2],
            "model": r[3],
            "warranty_period": r[4],
            "price_complete": float(r[5]),
            "quantity_accessories": r[6],
            "specifications": r[7] if r[7] else {},
            "created_at": r[8],
            "updated_at": r[9]
        } for r in rows]