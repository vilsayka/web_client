import json
from database import get_db_connection

def load_components_to_db(json_file):

    conn = get_db_connection()
    cur = conn.cursor()

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = ['processors', 'motherboards', 'gpus', 'psus', 'coolers', 'ram', 'storage', 'cases']

    for category in categories:
        components = data['components'][category]
        for comp in components:
            cur.execute("""
                INSERT INTO components (title, manufacturer, model, warranty_period, price_complete, quantity_accessories, specifications) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                comp['title'],
                comp['manufacturer'],
                comp['model'],
                comp['warranty_period'],
                comp['price_complete'],
                comp['quantity_accessories'],
                json.dumps(comp['specifications'], ensure_ascii=False)
            ))

    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    load_components_to_db(r'D:\web_client\db\scripts\tests_data.json')