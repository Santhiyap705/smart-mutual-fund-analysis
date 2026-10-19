import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_schemes, load_nav   # ✅ CSV based

st.set_page_config(layout="wide")

st.title("📊 Mutual Fund Analysis")

# -----------------------------
# CACHE (FAST ⚡)
# -----------------------------
@st.cache_data
def get_schemes():
    return load_schemes()

@st.cache_data
def get_nav(code):
    return load_nav(code)

# -----------------------------
# LOAD SCHEMES
# -----------------------------
fund_df = get_schemes()

if fund_df.empty or "Scheme Name" not in fund_df.columns:
    st.error("⚠ Unable to load schemes")
    st.stop()

# -----------------------------
# CATEGORY SELECT (FROM CSV)
# -----------------------------
st.markdown("### 📥 Select Category")

category_select = st.selectbox(
    "Category",
    sorted(fund_df["category"].unique())
)

# -----------------------------
# FILTER SCHEMES
# -----------------------------
filtered = fund_df[fund_df["category"] == category_select]

if filtered.empty:
    st.warning("No schemes found")
    st.stop()

# -----------------------------
# SHOW TOP 10 SCHEMES (FAST ⚡)
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
# LOAD NAV DATA
# -----------------------------
nav_df = get_nav(scheme_code)

if nav_df.empty:
    st.warning("⚠ No NAV data available")
    st.stop()

# -----------------------------
# NAV TREND
# -----------------------------
st.markdown("### 📈 NAV Trend")

fig = px.line(nav_df, x="date", y="nav")
st.plotly_chart(fig, width="stretch")

# -----------------------------
# CALCULATIONS
# -----------------------------
returns = nav_df["nav"].pct_change().dropna()

avg_return = returns.mean() * 100
risk = returns.std()

start_nav = nav_df["nav"].iloc[0]
end_nav = nav_df["nav"].iloc[-1]

years = (nav_df["date"].max() - nav_df["date"].min()).days / 365

cagr = ((end_nav / start_nav) ** (1 / years) - 1) * 100 if years > 0 else 0

# -----------------------------
# PERFORMANCE METRICS
# -----------------------------
st.markdown("### 📊 Performance")

col1, col2, col3 = st.columns(3)

col1.metric("Return (%)", round(avg_return, 2))
col2.metric("Risk", round(risk, 4))
col3.metric("CAGR (%)", round(cagr, 2))

# -----------------------------
# RISK LEVEL
# -----------------------------
st.markdown("### ⚠ Risk Level")

if risk < 0.01:
    st.success("Low Risk")
elif risk < 0.02:
    st.warning("Medium Risk")
else:
    st.error("High Risk")
