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
# Load Data (Cloud-Safe)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# Ensure datetime format
df["month"] = pd.to_datetime(df["month"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["month"].dt.year.unique())
)

df = df[df["month"].dt.year == year]

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

total_revenue = df["total_revenue"].sum()
avg_monthly_revenue = df["total_revenue"].mean()
best_month = df.loc[df["total_revenue"].idxmax(), "month"].strftime("%b %Y")

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
col3.metric("Best Month", best_month)

# -----------------------------
# Revenue Trend Chart
# -----------------------------
st.subheader("Monthly Revenue Trend")

fig = px.line(
    df,
    x="month",
    y="total_revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Revenue",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("Revenue Data")
st.dataframe(df, use_container_width=True)
