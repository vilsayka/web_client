from typing import List, Optional


def get_orders_by_customer(conn, customer_id: int) -> List[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT o.id_order, o.status_order, o.created_at, o.warranty_period,
                      o.id_importer,
                      imp.full_name as importer_name,
                      u_cust.user_name as customer_name
               FROM orders o
               JOIN users u_cust ON o.id_customer = u_cust.id_user
               LEFT JOIN importers imp ON o.id_importer = imp.id_importer
               WHERE o.id_customer = %s
               ORDER BY o.created_at DESC""",
            (customer_id,)
        )
        rows = cur.fetchall()
        return [{
            "id_order": r[0],
            "status_order": r[1],
            "created_at": r[2],
            "warranty_period": r[3],
            "id_importer": r[4],
            "importer_name": r[5],
            "customer_name": r[6]
        } for r in rows]


def get_orders_by_importer(conn, importer_id: int) -> List[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT o.id_order, o.status_order, o.created_at, o.warranty_period,
                      o.id_customer, o.id_importer,
                      imp.full_name as importer_name,
                      u_cust.user_name as customer_name
               FROM orders o
               JOIN users u_cust ON o.id_customer = u_cust.id_user
               JOIN importers imp ON o.id_importer = imp.id_importer
               WHERE o.id_importer = %s
               ORDER BY o.created_at DESC""",
            (importer_id,)
        )
        rows = cur.fetchall()
        return [{
            "id_order": r[0],
            "status_order": r[1],
            "created_at": r[2],
            "warranty_period": r[3],
            "id_customer": r[4],
            "id_importer": r[5],
            "importer_name": r[6],
            "customer_name": r[7]
        } for r in rows]


def get_order_by_id(conn, order_id: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT o.id_order, o.id_customer, o.id_importer, o.status_order,
                      o.date_assembly, o.warranty_period, o.created_at,
                      cu.user_name as customer_name,
                      imp.full_name as importer_name
               FROM orders o
               JOIN users cu ON o.id_customer = cu.id_user
               LEFT JOIN importers imp ON o.id_importer = imp.id_importer
               WHERE o.id_order = %s""",
            (order_id,)
        )
        row = cur.fetchone()
        if row:
            return {
                "id_order": row[0],
                "id_customer": row[1],
                "id_importer": row[2],
                "status_order": row[3],
                "date_assembly": row[4],
                "warranty_period": row[5],
                "created_at": row[6],
                "customer_name": row[7],
                "importer_name": row[8]
            }
    return None


def get_order_components(conn, order_id: int) -> List[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT c.id_component, c.title, c.manufacturer, c.model, c.price_complete,
                      pc.number_components
               FROM pc_composition pc
               JOIN components c ON pc.id_component = c.id_component
               WHERE pc.id_order = %s""",
            (order_id,)
        )
        rows = cur.fetchall()
        return [{
            "id_component": r[0],
            "title": r[1],
            "manufacturer": r[2],
            "model": r[3],
            "price": float(r[4]),
            "quantity": r[5]
        } for r in rows]


def get_available_orders(conn) -> List[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT o.id_order, o.status_order, o.created_at, o.warranty_period,
                      o.id_customer, u_cust.user_name as customer_name
               FROM orders o
               JOIN users u_cust ON o.id_customer = u_cust.id_user
               WHERE o.status_order = 'ожидает сборщика'
               ORDER BY o.created_at DESC"""
        )
        rows = cur.fetchall()
        return [{
            "id_order": r[0],
            "status_order": r[1],
            "created_at": r[2],
            "warranty_period": r[3],
            "id_customer": r[4],
            "customer_name": r[5]
        } for r in rows]