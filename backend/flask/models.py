from psycopg2.extras import DictCursor
import json
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.security import hash_password

def read_data_sort(conn, table_name, sort_column=None, sort_order='asc', search_column=None, search_value=None):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = f"SELECT * FROM {table_name}"
        params = []
        if search_column and search_column != "None" and search_value and search_value != "None":
            if search_value.isdigit():
                sql += f" WHERE {search_column} = {search_value}"
            else:
                sql += f" WHERE {search_column} ILIKE %s"
                params.append(f"%{search_value}%")
        if sort_column and sort_column != "None" and sort_column != "":
            order = "DESC" if sort_order and sort_order.lower() == 'desc' else "ASC"
            sql += f" ORDER BY {sort_column} {order}"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def update_data(conn, table_name, data):
    cur = conn.cursor()
    if table_name == 'users':
        cur.execute("UPDATE users SET user_name = %s, is_active = %s, user_role = %s WHERE id_user = %s",
                   (data['user_name'], data['is_active'], data['user_role'], data['id_user']))
    elif table_name == 'importers':
        cur.execute("UPDATE importers SET full_name = %s, telephone = %s, email = %s WHERE id_importer = %s",
                   (data['full_name'], data['telephone'], data['email'], data['id_importer']))
    elif table_name == 'orders':
        cur.execute("UPDATE orders SET status_order = %s, date_assembly = %s, warranty_period = %s WHERE id_order = %s",
                   (data['status_order'], data.get('date_assembly') or None, data['warranty_period'], data['id_order']))
    elif table_name == 'components':
        specs = data.get('specifications', {})
        if isinstance(specs, str):
            specs = json.loads(specs)
        cur.execute("UPDATE components SET title = %s, manufacturer = %s, model = %s, warranty_period = %s, price_complete = %s, quantity_accessories = %s, specifications = %s WHERE id_component = %s",
                   (data['title'], data['manufacturer'], data['model'], data['warranty_period'], data['price_complete'],
                    data['quantity_accessories'], json.dumps(specs, ensure_ascii=False), data['id_component']))
    elif table_name == 'service_guarantees':
        cur.execute("UPDATE service_guarantees SET date_repair_completion = %s, status_repair = %s WHERE id_repair_warranty = %s",
                   (data['date_repair_completion'], data['status_repair'], data['id_repair_warranty']))
    conn.commit()
    cur.close()

def add_data(conn, table_name, data):
    cur = conn.cursor()
    if table_name == 'users':
        hashed = hash_password(data['password_hash'])
        cur.execute("INSERT INTO users (user_name, password_hash) VALUES (%s, %s)",
                   (data['user_name'], hashed))
    elif table_name == 'importers':
        hashed = hash_password(data['password_hash'])
        cur.execute("INSERT INTO users (user_name, password_hash, user_role) VALUES (%s, %s, 'importer') RETURNING id_user",
                   (data['user_name'], hashed))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO importers (id_importer, full_name, telephone, email) VALUES (%s, %s, %s, %s)",
                   (user_id, data['full_name'], data['telephone'], data['email']))
    elif table_name == 'orders':
        cur.execute("INSERT INTO orders (id_customer, id_importer, warranty_period, status_order) VALUES (%s, %s, %s, %s)",
                   (data['id_customer'], data['id_importer'], data['warranty_period'], 'ожидает сборщика'))
    elif table_name == 'components':
        specs = data.get('specifications', {})
        if isinstance(specs, str):
            specs = json.loads(specs)
        cur.execute("INSERT INTO components (title, manufacturer, model, warranty_period, price_complete, quantity_accessories, specifications) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (data['title'], data['manufacturer'], data['model'], data['warranty_period'], data['price_complete'],
                    data['quantity_accessories'], json.dumps(specs, ensure_ascii=False)))
    elif table_name == 'service_guarantees':
        cur.execute("INSERT INTO service_guarantees (id_order, id_defective_component, Problem_description) VALUES (%s, %s, %s)",
                   (data['id_order'], data['id_defective_component'], data['Problem_description']))
    conn.commit()
    cur.close()