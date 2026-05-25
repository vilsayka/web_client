from typing import List


def create_guarantee(conn, order_id: int, defective_component_id: int, problem_description: str) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO service_guarantees (id_order, id_defective_component, problem_description)
               VALUES (%s, %s, %s)
               RETURNING id_repair_warranty, date_references, status_repair, created_at""",
            (order_id, defective_component_id, problem_description)
        )
        row = cur.fetchone()
    conn.commit()
    return {
        "id_repair_warranty": row[0],
        "id_order": order_id,
        "id_defective_component": defective_component_id,
        "date_references": row[1],
        "problem_description": problem_description,
        "status_repair": row[2],
        "created_at": row[3],
        "date_repair_completion": None
    }
      
        
def get_service_guarantees_by_user_id(conn, user_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT sg.id_repair_warranty,
                   sg.id_order,
                   sg.id_defective_component,
                   sg.date_references,
                   sg.problem_description,
                   sg.status_repair,
                   sg.created_at,
                   sg.date_repair_completion
            FROM service_guarantees sg
            JOIN orders o ON sg.id_order = o.id_order
            WHERE o.id_customer = %s
            ORDER BY sg.created_at DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()

    return [
        {
            "id_repair_warranty": row[0],
            "id_order": row[1],
            "id_defective_component": row[2],
            "date_references": row[3],
            "problem_description": row[4],
            "status_repair": row[5],
            "created_at": row[6],
            "date_repair_completion": row[7],
        }
        for row in rows
    ]