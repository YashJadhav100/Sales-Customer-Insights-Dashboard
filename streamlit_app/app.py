import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Interactive sales analytics built with Streamlit & Plotly")

# -------------------------------------------------
# Load Data (Cloud-safe paths)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MONTHLY_FILE = os.path.join(DATA_DIR, "monthly_revenue_trend.xlsx")

@st.cache_data
def load_data():
    df = pd.read_excel(MONTHLY_FILE)
    df["Month"] = pd.to_datetime(df["Month"])
    df["Year"] = df["Month"].dt.year
    df["Month_Name"] = df["Month"].dt.strftime("%b")
    return df

df = load_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

df_year = df[df["Year"] == year]

# -------------------------------------------------
# KPI Section (THIS WAS MISSING BEFORE)
# -------------------------------------------------
total_revenue = df_year["Revenue"].sum()
avg_monthly_revenue = df_year["Revenue"].mean()
best_month = df_year.loc[df_year["Revenue"].idxmax(), "Month"].strftime("%b %Y")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
col3.metric("Best Month", best_month)

st.divider()

# -------------------------------------------------
# Monthly Revenue Line Chart
# -------------------------------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_line = px.line(
    df_year,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# -------------------------------------------------
# Monthly Revenue Bar Chart (THIS WAS ERRORING)
# -------------------------------------------------
st.subheader("📊 Monthly Revenue Breakdown")

df_bar = df_year.copy()
df_bar["Month_Label"] = df_bar["Month"].dt.strftime("%b")

fig_bar = px.bar(
    df_bar,
    x="Month_Label",
    y="Revenue",
    text_auto=".2s",
    title="Revenue by Month"
)

fig_bar.update_layout(xaxis_title="Month", yaxis_title="Revenue")

st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -------------------------------------------------
# Data Table (THIS WAS ALSO MISSING)
# -------------------------------------------------
st.subheader("📄 Underlying Data")

st.dataframe(
    df_year.sort_values("Month"),
    use_container_width=True
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Built by Yash Jadhav | Streamlit Cloud Deployment")
