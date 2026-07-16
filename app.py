import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Coffee Product Optimization Dashboard",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Coffee Product Optimization & Revenue Dashboard")

# ---------------- Load Data ----------------
df = pd.read_excel("data/coffee.xlsx")
df["Hour"] = pd.to_datetime(
    df["transaction_time"], 
    format="%H:%M:%S"
).dt.hour

# Sidebar Filters
st.sidebar.header("Filters")

store = st.sidebar.multiselect(
    "Select Store",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["product_category"].unique(),
    default=df["product_category"].unique()
)

df = df[
    (df["store_location"].isin(store)) &
    (df["product_category"].isin(category))
]

st.success("Dataset Loaded Successfully!")

# ---------------- KPI ----------------
total_sales = (df["transaction_qty"] * df["unit_price"]).sum()
total_orders = len(df)
total_products = df["product_detail"].nunique()
total_stores = df["store_location"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue ($)", f"{total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Products", total_products)
col4.metric("Stores", total_stores)

st.divider()

# ---------------- Charts ----------------
col1, col2 = st.columns(2)

with col1:
    category = (
        df.groupby("product_category")["transaction_qty"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category,
        x="product_category",
        y="transaction_qty",
        title="Sales by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    location = (
        df.groupby("store_location")["transaction_qty"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        location,
        names="store_location",
        values="transaction_qty",
        title="Store Contribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Top 10 Selling Products")

top_products = (
    df.groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="product_detail",
    y="transaction_qty",
    color="transaction_qty",
    title="Top 10 Selling Products"
)

st.plotly_chart(fig3, use_container_width=True)

# Revenue by Category
df["Revenue"] = df["transaction_qty"] * df["unit_price"]

revenue = (
    df.groupby("product_category")["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    revenue,
    names="product_category",
    values="Revenue",
    title="Revenue by Category"
)

st.divider()

st.subheader("🏪 Revenue by Store")

store_revenue = (
    df.groupby("store_location")["Revenue"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    store_revenue,
    x="store_location",
    y="Revenue",
    color="Revenue",
    title="Revenue by Store"
)

st.plotly_chart(fig6, use_container_width=True)

st.plotly_chart(fig4, use_container_width=True)

st.divider()


csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="coffee_dashboard.csv",
    mime="text/csv"
)

st.subheader("Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

st.subheader("📌 Dashboard Insights")

st.write("""
• Coffee category generated the highest revenue.
• Morning hours (8 AM–10 AM) recorded maximum sales.
• Hell's Kitchen store generated the highest revenue.
• Top 10 products contribute significantly to overall sales.
• Filters help analyze store-wise and category-wise performance.
""")

st.divider()

st.subheader("⏰ Hour-wise Sales Analysis")

hourly_sales = (
    df.groupby("Hour")["transaction_qty"]
    .sum()
    .reset_index()
)

fig5 = px.line(
    hourly_sales,
    x="Hour",
    y="transaction_qty",
    markers=True,
    title="Sales by Hour"
)

st.plotly_chart(fig5, use_container_width=True)