import streamlit as st
import pandas as pd
from utils.data_loader import load_schemes, load_nav

st.title("💰 Smart SIP Investment Planner")

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

# ✅ FIX COLUMN NAMES
if fund_df.empty or "Scheme Name" not in fund_df.columns:
    st.error("⚠ Unable to load schemes")
    st.stop()

# -----------------------------
# CATEGORY SELECT
# -----------------------------
st.markdown("### 📥 Select Category")

category_select = st.selectbox(
    "Category",
    sorted(fund_df["category"].unique())
)

filtered = fund_df[fund_df["category"] == category_select]

if filtered.empty:
    st.warning("No schemes found")
    st.stop()

# -----------------------------
# SHOW 10 SCHEMES (FAST ⚡)
# -----------------------------
top_schemes = filtered.drop_duplicates().iloc[:10]

scheme = st.selectbox(
    "📌 Select Mutual Fund Scheme",
    top_schemes["Scheme Name"].tolist()
)

scheme_code = top_schemes[
    top_schemes["Scheme Name"] == scheme
]["SchemeCode"].values[0]

# -----------------------------
# LOAD NAV
# -----------------------------
with st.spinner("📊 Loading fund data..."):
    nav_df = get_nav(scheme_code)

if nav_df.empty:
    st.error("❌ No NAV data available")
    st.stop()

# -----------------------------
# CAGR CALCULATION
# -----------------------------
start_nav = nav_df["nav"].iloc[0]
end_nav = nav_df["nav"].iloc[-1]

years = (nav_df["date"].max() - nav_df["date"].min()).days / 365

cagr = ((end_nav / start_nav) ** (1 / years) - 1) * 100 if years > 0 else 10

# -----------------------------
# DISPLAY RETURN
# -----------------------------
st.success("✔ Return is automatically calculated using CAGR")
st.info(f"📊 Expected Return (CAGR): {round(cagr,2)}%")

# -----------------------------
# USER INPUT
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    monthly = st.number_input("💵 Monthly Investment (₹)", 500, value=1000)

with col2:
    years_input = st.slider("📅 Investment Duration (Years)", 1, 30, 10)

# -----------------------------
# SIP CALCULATION (NO ADJUST)
# -----------------------------
rate = cagr / 100 / 12
months = years_input * 12

if rate == 0:
    future_value = monthly * months
else:
    future_value = monthly * ((1 + rate)**months - 1) / rate * (1 + rate)

invested = monthly * months
profit = future_value - invested

# -----------------------------
# RESULTS
# -----------------------------
st.subheader("📈 Investment Summary")

c1, c2, c3 = st.columns(3)

c1.metric("Total Invested", f"₹{invested:,.0f}")
c2.metric("Estimated Value", f"₹{future_value:,.0f}")
c3.metric("Profit", f"₹{profit:,.0f}")

# -----------------------------
# CHART
# -----------------------------
chart_data = pd.DataFrame({
    "Type": ["Invested", "Profit"],
    "Amount": [invested, profit]
})

st.bar_chart(chart_data.set_index("Type"))

# -----------------------------
# INFO
# -----------------------------
st.warning("⚠ This is an estimated value based on historical returns.")
st.success("💡 Tip: Long-term investment gives better compounding growth!")
