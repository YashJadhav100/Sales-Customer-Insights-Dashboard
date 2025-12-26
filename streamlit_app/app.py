import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------
DATA_PATH = "data/monthly_revenue_trend.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("Filters")

years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

filtered_df = df[df["year"] == selected_year]

# ----------------------------
# Header
# ----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.markdown(
    """
    This interactive dashboard analyzes **retail sales performance and customer behavior**
    to uncover revenue trends and key business insights.
    """
)

st.divider()

# ----------------------------
# KPI Calculations
# ----------------------------
total_revenue = filtered_df["total_revenue"].sum()
avg_monthly_revenue = filtered_df["total_revenue"].mean()
best_month = filtered_df.loc[
    filtered_df["total_revenue"].idxmax(), "month"
]

total_orders = filtered_df["total_orders"].sum()
avg_order_value = total_revenue / total_orders

# ----------------------------
# KPI Cards
# ----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
col3.metric("Best Month", best_month)
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# ----------------------------
# Revenue Trend Chart
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig = px.line(
    filtered_df,
    x="month",
    y="total_revenue",
    markers=True,
    labels={"total_revenue": "Revenue ($)", "month": "Month"}
)

fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------
# Customer Insights
# ----------------------------
st.subheader("👥 Top Customers by Revenue")

if "customer_revenue" in filtered_df.columns:
    top_customers = (
        filtered_df.groupby("customer_id")["customer_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(top_customers, use_container_width=True)
else:
    st.info("Customer-level revenue not available in this dataset.")

st.divider()

# ----------------------------
# Data Table
# ----------------------------
st.subheader("📋 Full Dataset")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    """
    **Built by Yash Jadhav**  
    🔗 [GitHub Repository](https://github.com/YashJadhav100/Sales-Customer-Insights-Dashboard)
    """
)
