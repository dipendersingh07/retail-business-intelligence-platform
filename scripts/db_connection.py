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

def get_sales_trend(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            o.order_date,
            SUM(rp.selling_price * oi.quantity) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        JOIN retailer_products rp
            ON oi.retailer_product_id = rp.retailer_product_id
        JOIN retailers r
            ON o.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s
        GROUP BY o.order_date
        ORDER BY o.order_date;
    """

    cursor.execute(query, (retailer_name,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_top_products(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            p.product_name,
            SUM(oi.quantity) AS total_sold
        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN retailers r
            ON o.retailer_id = r.retailer_id

        JOIN retailer_products rp
            ON oi.retailer_product_id = rp.retailer_product_id

        JOIN products p
            ON rp.product_id = p.product_id

        WHERE r.retailer_name = %s

        GROUP BY p.product_name

        ORDER BY total_sold DESC

        LIMIT 5;
    """

    cursor.execute(query, (retailer_name,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_sales_by_category(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            c.category_name,
            SUM(oi.quantity * rp.selling_price) AS revenue

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN retailers r
            ON o.retailer_id = r.retailer_id

        JOIN retailer_products rp
            ON oi.retailer_product_id = rp.retailer_product_id

        JOIN products p
            ON rp.product_id = p.product_id

        JOIN categories c
            ON p.category_id = c.category_id

        WHERE r.retailer_name = %s

        GROUP BY c.category_name

        ORDER BY revenue DESC;
    """

    cursor.execute(query, (retailer_name,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_recent_orders(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            o.order_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer,
            o.order_date,
            o.payment_method,

            SUM(
                oi.quantity * rp.selling_price
            ) AS total

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN retailers r
            ON o.retailer_id = r.retailer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN retailer_products rp
            ON oi.retailer_product_id = rp.retailer_product_id

        WHERE r.retailer_name = %s

        GROUP BY
            o.order_id,
            customer,
            o.order_date,
            o.payment_method

        ORDER BY o.order_date DESC

        LIMIT 10;
    """

    cursor.execute(query, (retailer_name,))

    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return orders

def get_customers_by_city(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            c.city,
            COUNT(DISTINCT o.customer_id) AS customers
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN retailers r
            ON o.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s
        GROUP BY c.city
        ORDER BY customers DESC;
    """

    cursor.execute(query, (retailer_name,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_payment_methods(retailer_name):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            payment_method,
            COUNT(*) AS total
        FROM orders o
        JOIN retailers r
            ON o.retailer_id = r.retailer_id
        WHERE r.retailer_name = %s
        GROUP BY payment_method
        ORDER BY total DESC;
    """

    cursor.execute(query, (retailer_name,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_low_stock_products(retailer_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        p.product_name,
        rp.stock_quantity
    FROM retailer_products rp
    JOIN retailers r
        ON rp.retailer_id=r.retailer_id
    JOIN products p
        ON rp.product_id=p.product_id
    WHERE r.retailer_name=%s
    ORDER BY rp.stock_quantity
    LIMIT 5;
    """

    cursor.execute(query,(retailer_name,))
    data=cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_top_customers(retailer_name):
    connection=get_connection()

    cursor=connection.cursor(dictionary=True)

    query="""
    SELECT
        CONCAT(c.first_name,' ',c.last_name) customer,
        SUM(oi.quantity*rp.selling_price) total_spent

    FROM customers c

    JOIN orders o
        ON c.customer_id=o.customer_id

    JOIN order_items oi
        ON o.order_id=oi.order_id

    JOIN retailer_products rp
        ON oi.retailer_product_id=rp.retailer_product_id

    JOIN retailers r
        ON o.retailer_id=r.retailer_id

    WHERE r.retailer_name=%s

    GROUP BY customer

    ORDER BY total_spent DESC

    LIMIT 5;
    """

    cursor.execute(query,(retailer_name,))
    data=cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_monthly_sales(retailer_name):
    connection=get_connection()

    cursor=connection.cursor(dictionary=True)

    query="""
    SELECT
        DATE_FORMAT(o.order_date,'%Y-%m') month,
        SUM(oi.quantity*rp.selling_price) revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id=oi.order_id

    JOIN retailer_products rp
        ON oi.retailer_product_id=rp.retailer_product_id

    JOIN retailers r
        ON o.retailer_id=r.retailer_id

    WHERE r.retailer_name=%s

    GROUP BY month

    ORDER BY month;
    """

    cursor.execute(query,(retailer_name,))
    data=cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def get_inventory_summary(retailer_name):
    connection=get_connection()

    cursor=connection.cursor(dictionary=True)

    query="""
    SELECT
        COUNT(*) total_products,
        SUM(stock_quantity) total_stock,
        SUM(stock_quantity*selling_price) inventory_value

    FROM retailer_products rp

    JOIN retailers r
        ON rp.retailer_id=r.retailer_id

    WHERE r.retailer_name=%s;
    """

    cursor.execute(query,(retailer_name,))

    data=cursor.fetchone()

    cursor.close()
    connection.close()

    return data
