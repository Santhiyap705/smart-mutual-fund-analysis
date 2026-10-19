import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data_loader import load_schemes, load_nav
from models.nav_prediction import predict_nav

st.set_page_config(layout="wide")

st.title("🤖 NAV Prediction (2025–2030)")

# -----------------------------
# CACHE (FAST)
# -----------------------------
@st.cache_data
def get_schemes():
    return load_schemes()

@st.cache_data
def get_nav(code):
    return load_nav(code)

# -----------------------------
# LOAD DATA
# -----------------------------
fund_df = get_schemes()

if fund_df.empty or "Scheme Name" not in fund_df.columns:
    st.error("⚠ Unable to load data")
    st.stop()

# -----------------------------
# CATEGORY SELECT
# -----------------------------
st.markdown("### 📥 Select Fund Category")

category_select = st.selectbox(
    "Category",
    sorted(fund_df["category"].unique())
)

filtered = fund_df[fund_df["category"] == category_select]

if filtered.empty:
    st.warning("No schemes available")
    st.stop()

# -----------------------------
# SHOW 10 SCHEMES
# -----------------------------
top_schemes = filtered.drop_duplicates().iloc[:10]

scheme = st.selectbox(
    "📌 Select Scheme",
    top_schemes["Scheme Name"].tolist()
)

scheme_code = top_schemes[
    top_schemes["Scheme Name"] == scheme
]["SchemeCode"].values[0]

# -----------------------------
# LOAD NAV
# -----------------------------
nav_df = get_nav(scheme_code)

if nav_df.empty:
    st.warning("⚠ No NAV data")
    st.stop()

# -----------------------------
# PREDICT 5 YEARS (1825 days)
# -----------------------------
with st.spinner("🤖 Predicting NAV..."):
    forecast = predict_nav(nav_df, 5)

forecast["ds"] = pd.to_datetime(forecast["ds"])

# -----------------------------
# FUTURE DATA ONLY
# -----------------------------
future = forecast[forecast["ds"] > nav_df["date"].max()].copy()

# -----------------------------
# YEAR-WISE CONVERSION
# -----------------------------
future["year"] = future["ds"].dt.year
yearly_forecast = future.groupby("year").last().reset_index()

# -----------------------------
# FILTER 2025–2030
# -----------------------------
yearly_forecast = yearly_forecast[
    (yearly_forecast["year"] >= 2025) &
    (yearly_forecast["year"] <= 2030)
]

if yearly_forecast.empty:
    st.warning("⚠ Not enough data to show 2025–2030 prediction")
    st.stop()

# -----------------------------
# PLOT
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly_forecast["year"],
        y=yearly_forecast["yhat"],
        name="Predicted NAV (2025–2030)",
        mode="lines+markers"
    )
)

st.markdown("### 📈 Year-wise NAV Prediction (2025–2030)")

st.plotly_chart(fig, width="stretch")