import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.db_connection import (
    get_retailers,
    get_total_products,
    get_top_products,
    get_low_stock_products,
    get_inventory_summary,
)

st.set_page_config(
    page_title="Products",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

retailers = get_retailers()

selected_retailer = st.sidebar.selectbox(
    "Select Retailer",
    retailers,
    key="products"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

inventory = get_inventory_summary(selected_retailer)
top_products = get_top_products(selected_retailer)
low_stock = get_low_stock_products(selected_retailer)

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------

st.title("📦 Product Management")
st.caption(f"Retailer: {selected_retailer}")

st.divider()

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------

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

st.divider()

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Top Selling Products")

    top_df = pd.DataFrame(top_products)

    if not top_df.empty:

        top_df = top_df.sort_values(
            by="total_sold",
            ascending=True
        )

        fig = px.bar(
            top_df,
            x="total_sold",
            y="product_name",
            orientation="h",
            text="total_sold"
        )

        fig.update_traces(
            marker_color="#3B82F6",
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            showlegend=False,
            xaxis_title="Units Sold",
            yaxis_title="",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No product sales available.")

with right:

    st.subheader("Low Stock Products")

    low_df = pd.DataFrame(low_stock)

    if not low_df.empty:

        st.dataframe(
            low_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No low stock products.")

st.divider()

st.success("✅ Product dashboard loaded successfully.")