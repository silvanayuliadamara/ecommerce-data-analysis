
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_data
def load_data():
    main_data = pd.read_csv("dashboard/main_data.csv")
    rfm_data = pd.read_csv("dashboard/rfm_data.csv")
    state_analysis = pd.read_csv("dashboard/state_analysis.csv")
    category_analysis = pd.read_csv("dashboard/category_analysis.csv")

    main_data["order_purchase_timestamp"] = pd.to_datetime(main_data["order_purchase_timestamp"])

    return main_data, rfm_data, state_analysis, category_analysis

main_data, rfm_data, state_analysis, category_analysis = load_data()

st.title("🛒 E-Commerce Public Dataset Dashboard")
st.caption("Dashboard analisis revenue, kategori produk, segmentasi pelanggan, dan wilayah.")

min_date = main_data["order_purchase_timestamp"].min().date()
max_date = main_data["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.header("Filter Data")

    date_range = st.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    selected_state = st.multiselect(
        "Pilih State",
        options=sorted(main_data["customer_state"].dropna().unique()),
        default=None
    )

filtered_df = main_data.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["order_purchase_timestamp"].dt.date >= start_date) &
        (filtered_df["order_purchase_timestamp"].dt.date <= end_date)
    ]

if selected_state:
    filtered_df = filtered_df[filtered_df["customer_state"].isin(selected_state)]

total_revenue = filtered_df["revenue"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_unique_id"].nunique()
avg_review = filtered_df["review_score"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Average Review", f"{avg_review:.2f}")

st.divider()

st.subheader("Tren Revenue Bulanan")

monthly_revenue = filtered_df.groupby("order_month").agg({
    "revenue": "sum",
    "order_id": "nunique"
}).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_revenue["order_month"], monthly_revenue["revenue"], marker="o")
ax.set_title("Revenue Bulanan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Revenue")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.subheader("Top 10 Kategori Produk Berdasarkan Revenue")

category_revenue = (
    filtered_df.groupby("product_category_name_english")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 5))
category_revenue.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Kategori Produk")
ax.set_xlabel("Revenue")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

st.subheader("Top 10 State Berdasarkan Revenue")

state_revenue = (
    filtered_df.groupby("customer_state")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 5))
state_revenue.plot(kind="barh", ax=ax)
ax.set_title("Top 10 State")
ax.set_xlabel("Revenue")
ax.set_ylabel("State")
st.pyplot(fig)

st.subheader("Segmentasi Pelanggan RFM")

segment_summary = (
    rfm_data.groupby("segment")
    .agg(
        total_customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .reset_index()
    .sort_values("total_customers", ascending=False)
)

st.dataframe(segment_summary, use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 5))
segment_plot = segment_summary.sort_values("total_customers", ascending=True)
ax.barh(segment_plot["segment"], segment_plot["total_customers"])
ax.set_title("Jumlah Pelanggan per Segmen RFM")
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Segmen")
st.pyplot(fig)

st.subheader("Insight dan Rekomendasi")

st.write('''
1. Kategori produk dengan revenue tinggi dapat diprioritaskan untuk promosi dan pengelolaan stok.
2. Segmen pelanggan bernilai tinggi perlu dijaga melalui program loyalitas.
3. Pelanggan berisiko churn dapat diberikan promo reaktivasi.
4. Wilayah dengan kontribusi revenue besar dapat diprioritaskan untuk optimasi logistik dan pemasaran.
''')
