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
# Load Data (cloud-safe)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# -----------------------------
# Clean & Normalize Columns
# -----------------------------
df.columns = df.columns.str.strip().str.lower()

# Expecting something like: month, revenue, year
# Auto-detect month column
if "month" not in df.columns:
    st.error(f"❌ 'month' column not found. Columns available: {list(df.columns)}")
    st.stop()

if "revenue" not in df.columns:
    st.error(f"❌ 'revenue' column not found. Columns available: {list(df.columns)}")
    st.stop()

# Convert month safely
df["month"] = pd.to_datetime(df["month"])

# Add Year column if missing
if "year" not in df.columns:
    df["year"] = df["month"].dt.year

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

df_year = df[df["year"] == selected_year]

# -----------------------------
# Header
# -----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Monthly revenue performance and growth analysis")

# -----------------------------
# KPI Metrics
# -----------------------------
total_revenue = df_year["revenue"].sum()
avg_revenue = df_year["revenue"].mean()
best_month = df_year.loc[df_year["revenue"].idxmax(), "month"]

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_revenue:,.0f}")
col3.metric("Best Month", best_month.strftime("%b %Y"))

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_trend = px.line(
    df_year,
    x="month",
    y="revenue",
    markers=True,
    labels={"month": "Month", "revenue": "Revenue ($)"}
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# Month-over-Month Growth
# -----------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

df_year = df_year.sort_values("month")
df_year["mom_growth"] = df_year["revenue"].pct_change() * 100

fig_mom = px.bar(
    df_year,
    x="month",
    y="mom_growth",
    text_auto=".1f",
    labels={"mom_growth": "Growth (%)", "month": "Month"}
)

st.plotly_chart(fig_mom, use_container_width=True)

# -----------------------------
# Raw Data (Optional)
# -----------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(df_year)
