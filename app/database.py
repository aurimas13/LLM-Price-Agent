# app/database.py
import psycopg2
from psycopg2.extras import execute_batch

def get_db_connection():
    return psycopg2.connect(dbname='yourdbname', user='aurimasnausedas', host='localhost', password='newpassword')

def insert_products(conn, product):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products(title, description, vendor, type, tags, price, processed_description, entities)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                product["Title"],
                product["Description"],
                product["Vendor"],
                product["Type"],
                product["Tags"],
                product["Price"],
                product["Processed_Description"],
                product["Entities"]
            ))
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def find_similar_products(conn, query_vector, top_k=5):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, description, vendor, type, tags, price
            FROM products
            ORDER BY vendor <-> %s
            LIMIT %s
        """, (query_vector, top_k))
        return cur.fetchall()

def load_data_into_db(products_df):
    conn = get_db_connection()
    for index, row in products_df.iterrows():
        product = {
            "Title": row['Title'],
            "Description": row['Description'],
            "Vendor": row['Vendor'],
            "Type": row['Type'],  
            "Tags": ','.join(row['Tags']),  # Join the list of tags into a string
            "Price": row['Price'],
            "Processed_Description": row['Processed_Description'],
            "Entities": str(row['Entities'])  # Convert the list of entities to a string
        }
        insert_products(conn, product)
    conn.close()

    # Call the function with the path to your CSV   
    load_data_into_db('../data/products.csv')

