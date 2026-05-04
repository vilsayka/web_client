from database import get_db_connection
from psycopg2.extras import DictCursor

'''TABLE USERS'''

data_user = {"user_name": "kjhk",
        "password_hash": "password4",
        "token": "token"}

def add_user(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (user_name, password_hash, token) VALUES (%s, %s, %s)"
    cur.execute(sql, (userdata["user_name"], userdata["password_hash"], userdata["token"]))
    conn.commit()
    cur.close()
    conn.close()

#add_user(data_user)

def update_password_user(userdata):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE users SET password_hash = %s WHERE user_name = %s"
    cur.execute(sql, (userdata["password_hash"], userdata["user_name"]))
    
    conn.commit()
    cur.close()
    conn.close()
#update_password_user("sanya", data)

def read_data_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM users WHERE user_name = %s"
        cur.execute(sql, (username,))
        userdata = cur.fetchone()
        return dict(userdata)

    cur.close()
    conn.close()
    return userdata


'''TABLE IMPORTER'''

data_importer = {"user_name": "gjhgjgjhgjhg",
        "password_hash": "password4",
        "token": "token",
        "full_name": "Абв Где Жзи",
        "telephone": "+79011111111",
        "email": "hui@you.ez"}

def add_importer(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql_user = "INSERT INTO users (user_name, password_hash, token, user_role) VALUES (%s, %s, %s, 'importer') RETURNING id_user"
    cur.execute(sql_user, (userdata["user_name"], userdata["password_hash"], userdata["token"]))
    result = cur.fetchone()
    user_id = result[0]

    sql_importer = "INSERT INTO importers (id_importer, full_name, telephone, email) VALUES (%s, %s, %s, %s)"
    cur.execute(sql_importer, (user_id, userdata["full_name"], userdata["telephone"], userdata["email"]))

    conn.commit()
    cur.close()
    conn.close()

#add_importer(data_importer)

'''TABLE ORDERS'''

data_order = {"id_customer": "3",
        "id_importer": "password4",
        "date_order": "token",
        "date_assembly": "password4",
        "warranty_period": "34"}

def add_order(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO orders (id_customer, id_importer, date_order, date_assembly, warranty_period) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (userdata["user_name"], userdata["password_hash"], userdata["token"]))
    conn.commit()
    cur.close()
    conn.close()