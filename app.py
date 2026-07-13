import streamlit as st
import pandas as pd

from scripts.db_connection import (
    get_retailers,
    get_retailer_details,
    get_total_orders,
    get_total_products,
    get_total_revenue,
    get_total_customers,
    get_active_promotions,
    get_sales_trend,
    get_top_products,
    get_sales_by_category,
    get_recent_orders,
    get_customers_by_city,
    get_payment_methods,
    get_low_stock_products,
    get_top_customers,
    get_monthly_sales,
    get_inventory_summary,
)

st.set_page_config(
    page_title="Retail Business Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.title("📊 RBIP")
st.sidebar.markdown("---")

retailers = get_retailers()

selected_retailer = st.sidebar.selectbox(
    "Select Retailer",
    retailers
)
retailer = get_retailer_details(selected_retailer)
total_orders = get_total_orders(selected_retailer)
total_products = get_total_products(selected_retailer)
total_revenue = get_total_revenue(selected_retailer)
active_promotions = get_active_promotions(selected_retailer)
total_customers = get_total_customers(selected_retailer)
sales_trend = get_sales_trend(selected_retailer)
top_products = get_top_products(selected_retailer)
sales_by_category = get_sales_by_category(selected_retailer)
recent_orders = get_recent_orders(selected_retailer)
customers_by_city = get_customers_by_city(selected_retailer)
payment_methods = get_payment_methods(selected_retailer)
low_stock = get_low_stock_products(selected_retailer)
top_customers = get_top_customers(selected_retailer)
monthly_sales = get_monthly_sales(selected_retailer)
inventory = get_inventory_summary(selected_retailer)

st.sidebar.success("Database Connected")

# ---------------- Main Page ----------------

st.title("📊 Retail Business Intelligence Platform")

st.subheader("Retailer Information")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Retailer",
    retailer["retailer_name"]
)

col2.metric(
    "Headquarters",
    retailer["headquarters"]
)

col3.metric(
    "Country",
    retailer["country"]
)
st.divider()

st.subheader("Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Orders",
        total_orders
    )

with col2:
    st.metric(
        "Products Available",
        total_products
    )

with col3:
    st.metric(
        "Revenue",
        f"₹ {total_revenue:,.0f}"
    )

with col4:
    st.metric(
        "Active Promotions",
        active_promotions
    )

with col5:
    st.metric(
        "Customers",
        total_customers
    )

    st.markdown("---")
st.subheader("Revenue Trend")

df_sales = pd.DataFrame(sales_trend)

if not df_sales.empty:
    df_sales = df_sales.set_index("order_date")
    st.line_chart(df_sales["revenue"])
else:
    st.info("No sales data available.")

    st.markdown("---")
st.subheader("Top Selling Products")

df_products = pd.DataFrame(top_products)

if not df_products.empty:
    df_products = df_products.set_index("product_name")
    st.bar_chart(df_products["total_sold"])
else:
    st.info("No product sales available.")

    st.markdown("---")
st.subheader("Sales by Category")

df_category = pd.DataFrame(sales_by_category)

if not df_category.empty:
    df_category = df_category.set_index("category_name")
    st.bar_chart(df_category["revenue"])
else:
    st.info("No category sales available.")

    st.markdown("---")
st.subheader("Recent Orders")

df_orders = pd.DataFrame(recent_orders)

if not df_orders.empty:
    st.dataframe(
        df_orders,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No orders found.")

    st.markdown("---")

st.markdown("---")

st.subheader("Customer Distribution by City")

customer_df = pd.DataFrame(customers_by_city)

st.bar_chart(
    customer_df.set_index("city")
)

st.markdown("---")

st.subheader("Payment Method Distribution")

payment_df = pd.DataFrame(payment_methods)

if not payment_df.empty:
    payment_df = payment_df.set_index("payment_method")
    st.bar_chart(payment_df["total"])
else:
    st.info("No payment data available.")

    st.markdown("---")

st.subheader("Monthly Sales")

monthly_df = pd.DataFrame(monthly_sales)

if not monthly_df.empty:
    monthly_df = monthly_df.set_index("month")
    st.line_chart(monthly_df["revenue"])
else:
    st.info("No monthly sales available.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Low Stock Products")

    low_stock_df = pd.DataFrame(low_stock)

    if not low_stock_df.empty:
        st.dataframe(
            low_stock_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No low stock products.")

with col2:

    st.subheader("Top Customers")

    top_customer_df = pd.DataFrame(top_customers)

    if not top_customer_df.empty:
        st.dataframe(
            top_customer_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No customer data.")

st.markdown("---")

st.subheader("Inventory Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Products",
    inventory["total_products"]
)

c2.metric(
    "Units in Stock",
    inventory["total_stock"]
)

c3.metric(
    "Inventory Value",
    f"₹ {inventory['inventory_value']:,.0f}"
)