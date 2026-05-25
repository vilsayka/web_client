
from typing import Optional

def get_importer(conn, user_id: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT i.id_importer, i.full_name, i.telephone, i.email, i.created_at,
                   u.user_name, u.is_active
            FROM importers i
            JOIN users u ON i.id_importer = u.id_user
            WHERE i.id_importer = %s
        """, (user_id,))
        row = cur.fetchone()
        if row:
            return {
                "id_importer": row[0],
                "full_name": row[1],
                "telephone": row[2],
                "email": row[3],
                "created_at": row[4],
                "user_name": row[5],
                "is_active": row[6]
            }
        return None

def create_importer(conn, user_id: int, full_name: str, telephone: str, email: str) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO importers (id_importer, full_name, telephone, email) VALUES (%s, %s, %s, %s) RETURNING created_at",
            (user_id, full_name, telephone, email)
        )
        created_at = cur.fetchone()[0]
    conn.commit()
    return {"id_importer": user_id, "full_name": full_name, "telephone": telephone, "email": email, "created_at": created_at}