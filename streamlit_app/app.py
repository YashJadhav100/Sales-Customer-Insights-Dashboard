import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

# -----------------------------
# Load Data (Cloud-safe)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# Ensure correct types
df["month"] = pd.to_datetime(df["month"])
df = df.sort_values("month")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

df["year"] = df["month"].dt.year
year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

df_year = df[df["year"] == year]

# -----------------------------
# Title & Context
# -----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Monthly revenue performance and growth analysis")

st.divider()

# -----------------------------
# KPI Section
# -----------------------------
col1, col2, col3 = st.columns(3)

total_revenue = df_year["total_revenue"].sum()
avg_monthly_revenue = df_year["total_revenue"].mean()

best_month = df_year.loc[
    df_year["total_revenue"].idxmax(), "month"
].strftime("%b %Y")

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
col3.metric("Best Month", best_month)

st.divider()

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_revenue = px.line(
    df_year,
    x="month",
    y="total_revenue",
    markers=True,
    labels={"month": "Month", "total_revenue": "Revenue ($)"}
)

fig_revenue.update_layout(
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(fig_revenue, use_container_width=True)

# -----------------------------
# MoM Growth Chart (RESTORED)
# -----------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

fig_mom = px.bar(
    df_year,
    x="month",
    y="MoM Revenue Growth (%)",
    labels={
        "month": "Month",
        "MoM Revenue Growth (%)": "Growth (%)"
    },
    text_auto=".1f"
)

fig_mom.update_layout(
    xaxis_title="Month",
    yaxis_title="Growth (%)"
)

st.plotly_chart(fig_mom, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
with st.expander("📄 View Monthly Data"):
    st.dataframe(df_year, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    """
    **Built by Yash Jadhav**  
    🔗 [GitHub Repository](https://github.com/YashJadhav100/Sales-Customer-Insights-Dashboard)
    """
)
