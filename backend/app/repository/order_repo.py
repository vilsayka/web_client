
from typing import List


def create_order(conn, id_customer: int, warranty_period: int) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO orders (id_customer, warranty_period, status_order)
               VALUES (%s, %s, 'ожидает сборщика')
               RETURNING id_order, status_order, created_at, warranty_period, id_customer""",
            (id_customer, warranty_period)
        )
        row = cur.fetchone()
    conn.commit()
    return {
        "id_order": row[0],
        "id_customer": row[4],
        "id_importer": None,
        "status_order": row[1],
        "warranty_period": row[3],
        "created_at": row[2]
    }


def add_components_to_order(conn, order_id: int, component_ids: List[int]):
    with conn.cursor() as cur:
        for cid in component_ids:
            cur.execute(
                "INSERT INTO pc_composition (id_order, id_component, number_components) VALUES (%s, %s, 1)",
                (order_id, cid)
            )
    conn.commit()


def assign_importer(conn, order_id: int, importer_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE orders SET id_importer = %s, status_order = 'на сборке' "
            "WHERE id_order = %s AND id_importer IS NULL AND status_order = 'ожидает сборщика'",
            (importer_id, order_id)
        )
        updated = cur.rowcount
    conn.commit()
    return updated > 0


def update_order_status(conn, order_id: int, new_status: str, importer_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE orders SET status_order = %s WHERE id_order = %s AND id_importer = %s",
            (new_status, order_id, importer_id)
        )
        updated = cur.rowcount
    conn.commit()
    return updated > 0


def get_orders_stats(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT status_order, COUNT(*) FROM orders GROUP BY status_order")
        rows = cur.fetchall()
        return [{"status": r[0], "count": r[1]} for r in rows]