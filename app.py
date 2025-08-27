import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Retail Dashboard", layout="wide")

df = pd.read_csv("Retail_Transactions_2000.csv")

df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], errors="coerce")
df["DayOfWeek"] = df["PurchaseDate"].dt.day_name()


st.sidebar.header("🔍 Filters")

cities = st.sidebar.multiselect("Select City", options=df["City"].unique(), default=df["City"].unique())
categories = st.sidebar.multiselect("Select Product Category", options=df["ProductCategory"].unique(), default=df["ProductCategory"].unique())

filtered_df = df[(df["City"].isin(cities)) & (df["ProductCategory"].isin(categories))]


st.title("📊 Retail Transactions Dashboard")

total_sales = filtered_df["TotalAmount"].sum()
total_transactions = filtered_df.shape[0]
avg_order_value = round(total_sales / total_transactions, 2) if total_transactions > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("💰 Total Sales", f"₹ {total_sales:,.2f}")
kpi2.metric("🛒 Transactions", f"{total_transactions}")
kpi3.metric("📦 Avg Order Value", f"₹ {avg_order_value}")

st.subheader("📆 Sales by Day & Payment Mode")
fig1 = px.bar(
    filtered_df,
    x="DayOfWeek",
    y="TotalAmount",
    color="PaymentMode",
    title="Sales by Day & Payment Mode",
    category_orders={"DayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏙️ Sales by City")
fig2 = px.pie(
    filtered_df,
    names="City",
    values="TotalAmount",
    title="Sales Distribution by City"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📂 Sales by Product Category")
fig3 = px.bar(
    filtered_df.groupby("ProductCategory")["TotalAmount"].sum().reset_index(),
    x="ProductCategory",
    y="TotalAmount",
    title="Total Sales by Product Category"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📑 Transaction Data")
st.dataframe(filtered_df)

