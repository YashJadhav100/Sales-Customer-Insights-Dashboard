import os
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
# Load Data (Cloud-safe)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# Ensure proper types
df["Month"] = pd.to_datetime(df["Month"])
df["Year"] = df["Month"].dt.year
df["Month_Label"] = df["Month"].dt.strftime("%b %Y")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

df_year = df[df["Year"] == selected_year].copy()

# ----------------------------
# Header
# ----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Monthly revenue performance and growth analysis")

st.divider()

# ----------------------------
# KPIs
# ----------------------------
total_revenue = df_year["Revenue"].sum()
avg_monthly_revenue = df_year["Revenue"].mean()
best_month = df_year.loc[df_year["Revenue"].idxmax(), "Month_Label"]

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${total_revenue:,.0f}")
c2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
c3.metric("Best Month", best_month)

st.divider()

# ----------------------------
# Monthly Revenue Trend
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_trend = px.line(
    df_year,
    x="Month",
    y="Revenue",
    markers=True,
    labels={"Revenue": "Revenue ($)", "Month": "Month"}
)

fig_trend.update_layout(
    yaxis_tickprefix="$",
    height=450
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ----------------------------
# Month-over-Month Growth
# ----------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

df_year["MoM_Growth"] = df_year["Revenue"].pct_change() * 100

# Clean NaN / Inf values (CRITICAL FIX)
df_mom = df_year.replace([float("inf"), float("-inf")], None)
df_mom = df_mom.dropna(subset=["MoM_Growth"])

if df_mom.empty:
    st.warning("Not enough data to compute MoM growth.")
else:
    fig_mom = px.bar(
        df_mom,
        x="Month_Label",
        y="MoM_Growth",
        labels={
            "Month_Label": "Month",
            "MoM_Growth": "Growth (%)"
        }
    )

    fig_mom.update_layout(
        yaxis_ticksuffix="%",
        height=450
    )

    st.plotly_chart(fig_mom, use_container_width=True)

st.divider()

# ----------------------------
# Data Preview
# ----------------------------
with st.expander("📄 View Data"):
    st.dataframe(df_year, use_container_width=True)
