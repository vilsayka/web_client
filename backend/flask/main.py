import sys
import os
import json
from datetime import datetime

# Добавляем родительскую папку (backend) в путь, чтобы импортировать database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import get_master_connection, get_slave_connection
from models import read_data_sort, update_data, add_data

# Абсолютные пути к папкам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # backend/flask
template_dir = os.path.abspath(os.path.join(BASE_DIR, '../../frontend/templates'))
static_dir = os.path.abspath(os.path.join(BASE_DIR, '../../frontend/static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

TABLES = {
    'users': 'Пользователи',
    'importers': 'Импортеры',
    'orders': 'Заказы',
    'components': 'Комплектующие',
    'service_guarantees': 'Обращение по гарантии'
}

allowed_columns = {
    'users': ['id_user', 'user_name', 'user_role', 'created_at'],
    'importers': ['id_importer', 'full_name', 'telephone', 'email', 'created_at'],
    'orders': ['id_order', 'id_customer', 'id_importer', 'status_order', 'date_assembly', 'warranty_period', 'created_at'],
    'components': ['id_component', 'title', 'manufacturer', 'model', 'price_complete', 'quantity_accessories', 'created_at', 'updated_at'],
    'service_guarantees': ['id_repair_warranty', 'id_order', 'id_defective_component', 'date_references', 'date_repair_completion', 'status_repair', 'created_at']
}

allowed_columns_word = {
    'users': ['user_name', 'user_role'],
    'importers': ['full_name', 'telephone', 'email'],
    'orders': ['id_customer', 'id_importer', 'status_order'],
    'components': ['id_component', 'title', 'manufacturer', 'model', 'price_complete', 'quantity_accessories'],
    'service_guarantees': ['id_repair_warranty', 'id_order', 'id_defective_component', 'status_repair']
}

FIELDS_TEMPLATES = {
    "users": {
        "user_name": "Логин",
        "password_hash": "Пароль"
    },
    "importers": {
        "user_name": "Логин",
        "password_hash": "Пароль",
        "full_name": "ФИО",
        "telephone": "Телефон",
        "email": "Электронная почта"
    },
    "orders": {
        "id_customer": "Заказчик",
        "id_importer": "Сборщик",
        "warranty_period": "Срок гарантии (мес.)"
    },
    "service_guarantees": {
        "id_order": "Номер заказа",
        "id_defective_component": "Номер неисправной детали",
        "Problem_description": "Описание проблемы"
    },
    "components": {
        "manufacturer": "Производитель",
        "model": "Модель",
        "price_complete": "Цена",
        "quantity_accessories": "Количество",
        "warranty_period": "Гарантия (мес.)",
        "title": "Тип комплектующего",
        "specifications": "Характеристики"
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    table_name = 'users'
    sort_column = None
    sort_order = 'asc'
    search_column = None
    search_value = None

    if request.method == 'POST':
        table_name = request.form.get('table_name')
        sort_column = request.form.get('sort_column')
        sort_order = request.form.get('sort_order', 'asc')
        search_column = request.form.get('search_column')
        search_value = request.form.get('search_value')

    conn_slave = get_slave_connection()
    try:
        data = read_data_sort(conn_slave, table_name, sort_column, sort_order, search_column, search_value)
    finally:
        conn_slave.close()

    return render_template('main_page.html',
                           tables=TABLES,
                           table_data=data,
                           table_name=table_name,
                           sort_column=sort_column,
                           sort_order=sort_order,
                           search_column=search_column,
                           search_value=search_value,
                           allowed_columns=allowed_columns,
                           allowed_columns_word=allowed_columns_word)

@app.route('/add')
def add_page():
    return render_template('add.html')

@app.route('/add_form', methods=['POST'])
def add_form():
    table_name = request.form.get('table_name')
    fields = FIELDS_TEMPLATES.get(table_name, {})
    return render_template('add_form.html', fields=fields, table_name=table_name)

@app.route('/add_record', methods=['POST'])
def add_record():
    data = dict(request.form)
    if 'specifications_json' in data:
        specs_str = data['specifications_json'].replace('\r', '').replace('\n', '').replace('  ', '')
        data['specifications'] = json.loads(specs_str)
    data.pop('specifications_json', None)
    for key in list(data.keys()):
        if key.startswith('spec_'):
            data.pop(key, None)

    conn_master = get_master_connection()
    try:
        add_data(conn_master, data['table_name'], data)
    finally:
        conn_master.close()
    return redirect(url_for('index'))

@app.route('/details', methods=['POST'])
def details_post():
    table_name = request.form.get('table_name')
    row_json = request.form.get('row_data')
    row_data = json.loads(row_json)

    for date in ['date_assembly', 'date_repair_completion']:
        if date in row_data and row_data[date]:
            try:
                dt = datetime.strptime(row_data[date], '%a, %d %b %Y %H:%M:%S %Z')
                row_data[date] = dt.strftime('%Y-%m-%d')
            except:
                pass
    return render_template('update_details.html', row=row_data, table_name=table_name)

@app.route('/update', methods=['POST'])
def update_row():
    data = dict(request.form)
    table_name = data.get('table_name')
    if 'specifications' in data:
        data['specifications'] = json.loads(data['specifications'])
    conn_master = get_master_connection()
    try:
        update_data(conn_master, table_name, data)
    finally:
        conn_master.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)