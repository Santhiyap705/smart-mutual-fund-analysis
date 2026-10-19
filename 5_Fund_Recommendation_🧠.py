import streamlit as st
import pandas as pd
from utils.data_loader import load_schemes, load_nav
from models.recommendation import recommend_funds

st.title("🧠 Smart Fund Recommendation System")

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
# LOAD DATA
# -----------------------------
fund_df = get_schemes()

# ✅ FIX COLUMN NAMES
if fund_df.empty or "Scheme Name" not in fund_df.columns:
    st.error("⚠ Unable to load schemes")
    st.stop()

# -----------------------------
# USER INPUTS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    category = st.selectbox(
        "📊 Category",
        sorted(fund_df["category"].unique())
    )

with col2:
    risk_level = st.selectbox(
        "⚠ Risk Level",
        ["Low", "Medium", "High"]
    )

with col3:
    top_n = st.slider("🏆 Top Funds", 3, 10, 5)

# -----------------------------
# FILTER CATEGORY
# -----------------------------
filtered_funds = fund_df[fund_df["category"] == category]

if filtered_funds.empty:
    st.warning("No funds available in this category")
    st.stop()

# -----------------------------
# TAKE ONLY 10 SCHEMES (FAST ⚡)
# -----------------------------
filtered_funds = filtered_funds.drop_duplicates().iloc[:10]

st.info(f"Showing {category} funds with {risk_level} risk preference")

# -----------------------------
# PROCESS FUNDS
# -----------------------------
results = []

for _, row in filtered_funds.iterrows():

    try:
        nav_df = get_nav(row["SchemeCode"])

        if len(nav_df) < 5:   # small dataset support
            continue

        returns = nav_df["nav"].pct_change().dropna()

        avg_return = returns.mean() * 100
        risk = returns.std()

        # Risk classification
        if risk < 0.01:
            risk_tag = "Low"
        elif risk < 0.02:
            risk_tag = "Medium"
        else:
            risk_tag = "High"

        sharpe = avg_return / (risk + 0.0001)

        results.append({
            "Fund": row["Scheme Name"],
            "Return (%)": round(avg_return, 2),
            "Risk": round(risk, 4),
            "Risk Level": risk_tag,
            "Score": sharpe
        })

    except:
        continue

data = pd.DataFrame(results)

# -----------------------------
# FILTER BY RISK
# -----------------------------
if not data.empty:
    data = data[data["Risk Level"] == risk_level]

# -----------------------------
# SHOW RESULTS
# -----------------------------
if data.empty:
    st.error("❌ No funds match your selection")

else:
    # Format for model
    data = data.rename(columns={
        "Return (%)": "return",
        "Risk": "risk",
        "Score": "sharpe"
    })

    rec = recommend_funds(data)

    # Back to display format
    rec = rec.rename(columns={
        "return": "Return (%)",
        "risk": "Risk",
        "sharpe": "Score"
    })

    rec = rec.sort_values(by="Score", ascending=False)

    st.subheader(f"🏆 Top {top_n} Recommended Funds")

    st.dataframe(
        rec.head(top_n),
        use_container_width=True
    )

    # ⭐ Best Fund
    st.success(f"⭐ Best Fund: {rec.iloc[0]['Fund']}")

    st.success("✅ Recommendation based on Return, Risk & Sharpe Ratio")

# -----------------------------
# INSIGHT
# -----------------------------
st.markdown("### 📊 Insight")

st.write("""
- Higher return funds may have higher risk  
- Low risk funds are more stable but give lower returns  
- Best fund depends on your investment goal and duration  
""")