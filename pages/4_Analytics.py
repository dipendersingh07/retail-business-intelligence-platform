import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.db_connection import (
    get_retailers,
    get_total_revenue,
    get_sales_trend,
    get_sales_by_category,
    get_top_products,
    get_monthly_sales,
)

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

retailers = get_retailers()

selected_retailer = st.sidebar.selectbox(
    "Select Retailer",
    retailers,
    key="analytics"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

total_revenue = get_total_revenue(selected_retailer)
sales_trend = get_sales_trend(selected_retailer)
sales_category = get_sales_by_category(selected_retailer)
top_products = get_top_products(selected_retailer)
monthly_sales = get_monthly_sales(selected_retailer)

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("📈 Business Analytics")
st.caption(f"Retailer: {selected_retailer}")

st.divider()

# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

st.metric(
    "Total Revenue",
    f"₹ {total_revenue:,.0f}"
)

st.divider()

# ---------------------------------------------------------
# Revenue Trend
# ---------------------------------------------------------

st.subheader("Revenue Trend")

trend_df = pd.DataFrame(sales_trend)

if not trend_df.empty:

    fig = px.line(
        trend_df,
        x="order_date",
        y="revenue",
        markers=True
    )

    fig.update_traces(
        line_color="#2563EB"
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        xaxis_title="Date",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No revenue data available.")

st.divider()

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Sales by Category")

    category_df = pd.DataFrame(sales_category)

    if not category_df.empty:

        fig = px.bar(
            category_df,
            x="category_name",
            y="revenue",
            color="revenue",
            text="revenue"
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=False,
            height=420,
            xaxis_title="Category",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No category data available.")

with right:

    st.subheader("Top Selling Products")

    product_df = pd.DataFrame(top_products)

    if not product_df.empty:

        product_df = product_df.sort_values(
            by="total_sold",
            ascending=True
        )

        fig = px.bar(
            product_df,
            x="total_sold",
            y="product_name",
            orientation="h",
            text="total_sold"
        )

        fig.update_traces(
            marker_color="#10B981",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=False,
            height=420,
            xaxis_title="Units Sold",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No product data available.")

st.divider()

# ---------------------------------------------------------
# Monthly Sales
# ---------------------------------------------------------

st.subheader("Monthly Sales")

monthly_df = pd.DataFrame(monthly_sales)

if not monthly_df.empty:

    fig = px.area(
        monthly_df,
        x="month",
        y="revenue"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
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

st.success("✅ Analytics dashboard loaded successfully.")