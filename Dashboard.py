import streamlit as st
import pandas as pd
import plotly.express as px

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
    page_icon="assets/images/rbip_logo.png",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.logo("assets/images/rbip_logo.png")

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

# =======================
# Row 1
# =======================

left, right = st.columns(2)

    # ======================================================
# Analytics Dashboard
# ======================================================


# ---------------- Row 1 ----------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Revenue Trend")

    df_sales = pd.DataFrame(sales_trend)

    if not df_sales.empty:

        fig = px.line(
            df_sales,
            x="order_date",
            y="revenue",
            markers=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20),
            xaxis_title="Date",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No sales data available.")

with col2:

    st.subheader("Monthly Sales")

    monthly_df = pd.DataFrame(monthly_sales)

    if not monthly_df.empty:

        fig = px.line(
            monthly_df,
            x="month",
            y="revenue",
            markers=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No monthly sales available.")

# ---------------- Row 2 ----------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Selling Products")

    df_products = pd.DataFrame(top_products)

    if not df_products.empty:

        fig = px.bar(
            df_products,
            x="total_sold",
            y="product_name",
            orientation="h",
            text="total_sold"
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20),
            xaxis_title="Units Sold",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No product sales available.")

with col2:

    st.subheader("Sales by Category")

    df_category = pd.DataFrame(sales_by_category)

    if not df_category.empty:

        fig = px.pie(
            df_category,
            names="category_name",
            values="revenue",
            hole=.55
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No category sales.")

# ---------------- Row 3 ----------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Customer Distribution")

    customer_df = pd.DataFrame(customers_by_city)

    if not customer_df.empty:

        fig = px.bar(
            customer_df,
            x="customers",
            y="city",
            orientation="h",
            text="customers"
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20),
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Payment Method Distribution")

    payment_df = pd.DataFrame(payment_methods)

    if not payment_df.empty:

        fig = px.pie(
            payment_df,
            names="payment_method",
            values="total",
            hole=.55
        )

        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20,r=20,t=20,b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- Row 4 ----------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Low Stock Products")

    st.dataframe(
        pd.DataFrame(low_stock),
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.subheader("Top Customers")

    st.dataframe(
        pd.DataFrame(top_customers),
        use_container_width=True,
        hide_index=True
    )

# ---------------- Recent Orders ----------------

st.markdown("---")

st.subheader("Recent Orders")

st.dataframe(
    pd.DataFrame(recent_orders),
    use_container_width=True,
    hide_index=True
)

# ---------------- Inventory ----------------

st.markdown("---")

st.subheader("Inventory Summary")

c1, c2, c3 = st.columns(3)

c1.metric("Products", inventory["total_products"])
c2.metric("Units in Stock", inventory["total_stock"])
c3.metric("Inventory Value", f"₹ {inventory['inventory_value']:,.0f}")