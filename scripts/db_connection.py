import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def get_retailers():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT retailer_name
        FROM retailers
        ORDER BY retailer_name;
    """)

    retailers = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return retailers

def get_retailer_details(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            retailer_name,
            headquarters,
            country
        FROM retailers
        WHERE retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    retailer = cursor.fetchone()

    cursor.close()
    connection.close()

    return retailer

def get_total_orders(retailer_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM orders o
        JOIN retailers r
            ON o.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    total_orders = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_orders
def get_total_products(retailer_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM retailer_products rp
        JOIN retailers r
            ON rp.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    total_products = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_products
def get_total_revenue(retailer_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT
            COALESCE(SUM(rp.selling_price * oi.quantity), 0)
        FROM order_items oi
        JOIN retailer_products rp
            ON oi.retailer_product_id = rp.retailer_product_id
        JOIN retailers r
            ON rp.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return revenue

def get_active_promotions(retailer_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM promotions p
        JOIN retailer_products rp
            ON p.retailer_product_id = rp.retailer_product_id
        JOIN retailers r
            ON rp.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total

def get_total_customers(retailer_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT COUNT(DISTINCT customer_id)
        FROM orders o
        JOIN retailers r
            ON o.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s;
    """

    cursor.execute(query, (retailer_name,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total