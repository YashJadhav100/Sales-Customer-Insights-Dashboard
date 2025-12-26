import os
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Monthly revenue performance and growth analysis")

# --------------------------------------------------
# Load Data (Cloud-safe path)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# --------------------------------------------------
# Normalize column names (IMPORTANT)
# --------------------------------------------------
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_cols = {"month", "total_revenue"}
if not required_cols.issubset(df.columns):
    st.error(f"Dataset must contain columns: {required_cols}")
    st.stop()

# Convert month column to datetime
df["month"] = pd.to_datetime(df["month"])

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["month"].dt.year.unique())
)

df_year = df[df["month"].dt.year == selected_year].sort_values("month")

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------
df_year["mom_growth_pct"] = df_year["total_revenue"].pct_change() * 100

# --------------------------------------------------
# KPI Section
# --------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "Total Revenue",
    f"${df_year['total_revenue'].sum():,.0f}"
)

k2.metric(
    "Avg Monthly Revenue",
    f"${df_year['total_revenue'].mean():,.0f}"
)

best_month = df_year.loc[df_year["total_revenue"].idxmax(), "month"].strftime("%b %Y")
k3.metric("Best Month", best_month)

st.divider()

# --------------------------------------------------
# Monthly Revenue Trend
# --------------------------------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_trend = px.line(
    df_year,
    x="month",
    y="total_revenue",
    markers=True
)

fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)

st.plotly_chart(fig_trend, use_container_width=True)

# --------------------------------------------------
# Month-over-Month Growth
# --------------------------------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

fig_mom = px.bar(
    df_year,
    x="month",
    y="mom_growth_pct",
    text_auto=".1f"
)

fig_mom.update_layout(
    xaxis_title="Month",
    yaxis_title="Growth (%)"
)

st.plotly_chart(fig_mom, use_container_width=True)

# --------------------------------------------------
# Data Preview
# --------------------------------------------------
with st.expander("📄 View Data"):
    st.dataframe(df_year, use_container_width=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("Built with Streamlit, Pandas, and Plotly")
