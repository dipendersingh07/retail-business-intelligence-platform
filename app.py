import streamlit as st
from scripts.db_connection import (
    get_retailers,
    get_retailer_details
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