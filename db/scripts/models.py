from database import get_db_connection
from psycopg2.extras import DictCursor
import json

'''TABLE USERS'''

data_user = {
    "user_name": "kjhk",
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
    
    sql = "UPDATE users SET password_hash = %s WHERE id_user = %s"
    cur.execute(sql, (userdata["password_hash"], userdata["id_user"]))
    
    conn.commit()
    cur.close()
    conn.close()
#update_password_user(data_user)

def update_data_user(userdata):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE users SET is_active = %s, user_role= %s WHERE id_user = %s"
    cur.execute(sql, (userdata["is_active"], userdata["user_role"], userdata["id_user"]))
    
    conn.commit()
    cur.close()
    conn.close()
#update_data_user(data_user)

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

def read_data_user():
    conn = get_db_connection() 
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM users"
        cur.execute(sql)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    cur.close()
    conn.close()

'''TABLE IMPORTERS'''

data_importer = {
    "user_name": "gjhvcxg",
    "password_hash": "password4",
    "token": "token",
    "full_name": "Абв Где Жи",
    "telephone": "+7901111111",
    "email": "hi@you.ez"
    }

def add_importer(userdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql_user = "INSERT INTO users (user_name, password_hash, user_role) VALUES (%s, %s, 'importer') RETURNING id_user"
    cur.execute(sql_user, (userdata["user_name"], userdata["password_hash"]))
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
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    cur.close()
    conn.close()

'''TABLE ORDERS'''

data_order = {
    "id_order": "1",
    "id_customer": "1",
    "id_importer": "2",
    "date_order": "token",
    "status_order": "сформирована",
    "warranty_period": "34"
    }

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
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    cur.close()
    conn.close()

#print(read_data_order())

def update_data_order(data_order):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE orders SET status_order = %s, date_assembly= %s, warranty_period= %s WHERE id_order = %s"
    cur.execute(sql, (data_order["status_order"], data_order["date_assembly"], data_order["warranty_period"], data_order["id_order"]))
    
    conn.commit()
    cur.close()
    conn.close()
    
#update_data_order(data_order)


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

#add_service_guarantees(data_service_guarantees)

def update_data_service_guarantees(data_order):
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = "UPDATE service_guarantees SET date_repair_completion = %s, status_repair = %s WHERE id_repair_warranty = %s"
    cur.execute(sql, (data_order["date_repair_completion"], data_order["status_repair"], data_order["id_repair_warranty"]))
    
    conn.commit()
    cur.close()
    conn.close()
    
#update_status_service_guarantees(data_service_guarantees)

def read_data_service_guarantees():
    conn = get_db_connection()
    cur = conn.cursor()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM service_guarantees"
        cur.execute(sql)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    cur.close()
    conn.close()

#print(read_data_service_guarantees())

'''TABLE COMPONENTS'''

data_components = {
    "id_component": "56",
    "title": "Graphics Card",
    "manufacturer": "NVIDIA",
    "model": "RTX 4090",
    "warranty_period": 36,
    "price_complete": 159990.00,
    "quantity_accessories": 3,
    "specifications": {
    "tdp_w": 450,
    "recommended_psu_w": 1000,
    "length_mm": 348,
    "thickness_slots": 3.5,
    "pcie_power_pins": "12VHPWR",
    "pcie_version": 4.0,
    "vram_gb": 24,
    "vram_type": "GDDR6X"}
    }

def add_components(componentdata):

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "INSERT INTO components (title, manufacturer, model, warranty_period, price_complete, quantity_accessories, specifications) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    specifications_json = json.dumps(componentdata["specifications"], ensure_ascii=False)

    cur.execute(sql, (componentdata["title"], componentdata["manufacturer"], componentdata["model"], componentdata["warranty_period"], componentdata["price_complete"], componentdata["quantity_accessories"], specifications_json))
    conn.commit()
    cur.close()
    conn.close()

#add_components(data_components)

def update_components(componentdata):
    conn = get_db_connection()
    cur = conn.cursor()
    
    specifications_json = json.dumps(componentdata["specifications"], ensure_ascii=False)

    sql = """UPDATE components SET title = %s, manufacturer = %s, model = %s, warranty_period = %s, price_complete = %s, quantity_accessories = %s, specifications = %s WHERE id_component = %s"""
    cur.execute(sql, (componentdata["title"], componentdata["manufacturer"], componentdata["model"], componentdata["warranty_period"], componentdata["price_complete"], componentdata["quantity_accessories"], specifications_json, componentdata["id_component"]))
    
    conn.commit()
    cur.close()
    conn.close()
    
#update_components(data_components)

def read_data_components():
    conn = get_db_connection()
    cur = conn.cursor()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM components"
        cur.execute(sql)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    cur.close()
    conn.close()

#print(read_data_components())