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