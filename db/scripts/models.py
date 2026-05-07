from database import get_db_connection
from psycopg2.extras import DictCursor

'''TABLE USERS'''

data_user = {"user_name": "kjhk",
        "password_hash": "password4"
        }
def add_user(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (user_name, password_hash) VALUES (%s, %s)"
    cur.execute(sql, (userdata["user_name"], userdata["password_hash"]))
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

'''TABLE IMPORTERS'''

data_importer = {"user_name": "gjhgjgjhgjhg",
        "password_hash": "password4",
        "token": "token",
        "full_name": "Абв Где Жи",
        "telephone": "+7901111111",
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

def update_importer(data_importer):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE importers SET full_name = %s, telephone = %s, email = %s WHERE id_importer = %s"
    cur.execute(sql, (data_importer["full_name"], data_importer["telephone"], data_importer["email"],data_importer["id_importer"]))
    
    conn.commit()
    cur.close()
    conn.close()

#update_importer(data_importer)

def read_data_importer():
    conn = get_db_connection()
    cur = conn.cursor()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM importers"
        cur.execute(sql)
        userdata = cur.fetchone()
        return dict(userdata)

    cur.close()
    conn.close()
    return userdata

'''TABLE ORDERS'''

data_order = {"id_order": "1",
        "id_customer": "1",
        "id_importer": "2",
        "date_order": "token",
        "status_order": "сформирована",
        "warranty_period": "34"}

def add_order(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO orders (id_customer, id_importer, warranty_period, status_order) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (userdata["id_customer"], userdata["id_importer"], userdata["warranty_period"], "сформирована"))
    conn.commit()
    cur.close()
    conn.close()

#add_order(data_order)

def read_data_order():
    conn = get_db_connection()
    cur = conn.cursor()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM orders"
        cur.execute(sql)
        userdata = cur.fetchone()
        return dict(userdata)

    cur.close()
    conn.close()
    return userdata

#print(read_data_order())

def update_status_order(data_order):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE orders SET status_order = %s WHERE id_order = %s"
    cur.execute(sql, (data_order["status_order"], data_order["id_order"]))
    
    conn.commit()
    cur.close()
    conn.close()
    
#update_status_order(data_order)

'''TABLE SERVICE_GUARANTEES'''

data_service_guarantees = {
        "id_repair_warranty": "2",
        "id_order": "1",
        "id_defective_component": "1",
        "Problem_description": "всё хуйня",
        "status_order": 'rejected',
        }

def add_service_guarantees(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO service_guarantees (id_order, id_defective_component, Problem_description) VALUES (%s, %s, %s)"
    cur.execute(sql, (userdata["id_order"], userdata["id_defective_component"], userdata["Problem_description"]))
    conn.commit()
    cur.close()
    conn.close()

add_service_guarantees(data_service_guarantees)

def update_status_service_guarantees(data_order):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE service_guarantees SET status_repair = %s WHERE id_repair_warranty = %s"
    cur.execute(sql, (data_order["status_order"], data_order["id_repair_warranty"]))
    
    conn.commit()
    cur.close()
    conn.close()
    
#update_status_service_guarantees(data_service_guarantees)