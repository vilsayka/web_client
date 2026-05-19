import psycopg2
from config import DATABASE_URL_MASTER, DATABASE_URL_SLAVE  
def check(url, name):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print(f"✅ {name} ({url}) — OK")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ {name} ({url}) — ошибка: {e}")

if __name__ == "__main__":
    check(DATABASE_URL_MASTER, "Master")
    check(DATABASE_URL_SLAVE, "Slave")