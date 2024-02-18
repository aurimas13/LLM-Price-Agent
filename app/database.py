# app/database.py
import psycopg2
from psycopg2.extras import execute_batch

def get_db_connection():
    return psycopg2.connect(dbname='yourdbname', user='youruser', host='yourhost', password='yourpassword')

def insert_product_vector(conn, product):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO product_vectors (title, description, vector, price, tags)
            VALUES (%s, %s, %s, %s, %s)
        """, (product["title"], product["description"], product["vector"], product["price"], product["tags"]))
        conn.commit()


def find_similar_products(conn, query_vector, top_k=5):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, description, price, tags
            FROM product_vectors
            ORDER BY vector <-> %s
            LIMIT %s
        """, (query_vector, top_k))
        return cur.fetchall()

def load_data_into_db(products_df, model):
    conn = get_db_connection()
    for index, row in products_df.iterrows():
        product_vector = model.encode(row['Processed_Description']).tolist()
        product = {
            "title": row['Title'],
            "description": row['Cleaned_Description'],
            "vector": product_vector
        }
        insert_product_vector(conn, product)
    conn.close()