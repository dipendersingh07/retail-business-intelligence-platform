import streamlit as st
import pandas as pd

from scripts.db_connection import (
    get_retailers,
    get_retailer_details,
    get_total_orders,
    get_total_products,
    get_total_revenue,
    get_active_promotions,
    get_total_customers,
    get_sales_trend,
    get_top_products
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