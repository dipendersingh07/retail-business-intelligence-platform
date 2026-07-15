import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.db_connection import (
    get_retailers,
    get_total_orders,
    get_payment_methods,
    get_recent_orders,
    get_monthly_sales,
)

st.set_page_config(
    page_title="Orders",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

retailers = get_retailers()

selected_retailer = st.sidebar.selectbox(
    "Select Retailer",
    retailers,
    key="orders"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

total_orders = get_total_orders(selected_retailer)
payment_methods = get_payment_methods(selected_retailer)
recent_orders = get_recent_orders(selected_retailer)
monthly_sales = get_monthly_sales(selected_retailer)

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("🛒 Order Management")
st.caption(f"Retailer: {selected_retailer}")

st.divider()

# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

st.metric(
    "Total Orders",
    total_orders
)

st.divider()

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Payment Method Distribution")

    payment_df = pd.DataFrame(payment_methods)

    if not payment_df.empty:

        fig = px.pie(
            payment_df,
            values="total",
            names="payment_method",
            hole=0.45
        )

        fig.update_layout(
            height=420,
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No payment data available.")

with right:

    st.subheader("Monthly Sales")

    monthly_df = pd.DataFrame(monthly_sales)

    if not monthly_df.empty:

        fig = px.line(
            monthly_df,
            x="month",
            y="revenue",
            markers=True
        )

        fig.update_traces(
            line_color="#3B82F6"
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            xaxis_title="Month",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No monthly sales available.")

st.divider()

# ---------------------------------------------------------
# Recent Orders
# ---------------------------------------------------------

st.subheader("Recent Orders")

orders_df = pd.DataFrame(recent_orders)

if not orders_df.empty:

    orders_df["total"] = orders_df["total"].map(
        lambda x: f"₹ {x:,.2f}"
    )

    st.dataframe(
        orders_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No orders found.")

st.divider()

st.success("✅ Order dashboard loaded successfully.")