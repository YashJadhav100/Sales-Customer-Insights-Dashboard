import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Interactive analysis of monthly revenue trends and growth")

# -----------------------------
# Load data
# -----------------------------
DATA_PATH = "data/monthly_revenue_trend.xlsx"
df = pd.read_excel(DATA_PATH)

# Ensure datetime
df["month"] = pd.to_datetime(df["month"])

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["month"].dt.year.unique())
)

df = df[df["month"].dt.year == year]

# -----------------------------
# Feature engineering
# -----------------------------
df = df.sort_values("month")
df["MoM_Growth_%"] = df["total_revenue"].pct_change() * 100

# -----------------------------
# KPI Section
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${df['total_revenue'].sum():,.0f}"
)

col2.metric(
    "Avg Monthly Revenue",
    f"${df['total_revenue'].mean():,.0f}"
)

best_month = df.loc[df["total_revenue"].idxmax(), "month"].strftime("%b %Y")
col3.metric(
    "Best Month",
    best_month
)

st.divider()

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_trend = px.line(
    df,
    x="month",
    y="total_revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Revenue ($)",
    hovermode="x unified"
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# MoM Growth
# -----------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

fig_mom = px.bar(
    df,
    x="month",
    y="MoM_Growth_%",
    title="MoM Revenue Growth (%)",
    text_auto=".1f"
)

fig_mom.update_layout(
    xaxis_title="Month",
    yaxis_title="Growth (%)"
)

st.plotly_chart(fig_mom, use_container_width=True)

# -----------------------------
# Data Preview
# -----------------------------
with st.expander("📄 View Data"):
    st.dataframe(df, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.caption("Built with Streamlit, Pandas, and Plotly")
