from database import get_db_connection

def create_user(username, password_hash):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = f"INSERT INTO users (user_name, password_hash) VALUES (%s, %s)"
    cur.execute(sql, (username, password_hash))
    conn.commit()
