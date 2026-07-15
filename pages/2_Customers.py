import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.db_connection import (
    get_retailers,
    get_total_customers,
    get_customers_by_city,
    get_top_customers,
)

st.set_page_config(
    page_title="Customers",
    page_icon="👥",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

retailers = get_retailers()

selected_retailer = st.sidebar.selectbox(
    "Select Retailer",
    retailers,
    key="customers"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

total_customers = get_total_customers(selected_retailer)
customers_by_city = get_customers_by_city(selected_retailer)
top_customers = get_top_customers(selected_retailer)

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------

st.title("👥 Customer Management")
st.caption(f"Retailer: {selected_retailer}")

st.divider()

# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

st.metric(
    "Total Customers",
    total_customers
)

st.divider()

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Customer Distribution by City")

    city_df = pd.DataFrame(customers_by_city)

    if not city_df.empty:

        city_df = city_df.sort_values(
            by="customers",
            ascending=True
        )

        fig = px.bar(
            city_df,
            x="customers",
            y="city",
            orientation="h",
            text="customers"
        )

        fig.update_traces(
            marker_color="#10B981",
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            showlegend=False,
            xaxis_title="Customers",
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

        st.info("No customer data available.")

with right:

    st.subheader("Top Customers")

    customer_df = pd.DataFrame(top_customers)

    if not customer_df.empty:

        customer_df["total_spent"] = customer_df["total_spent"].map(
            lambda x: f"₹ {x:,.2f}"
        )

        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No customer purchases found.")

st.divider()

st.success("✅ Customer dashboard loaded successfully.")