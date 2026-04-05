import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        user="postgres", 
        password="vibecore",      
        database="vibecore",
        client_encoding='UTF8' 
    )