import streamlit as st

st.set_page_config(layout="wide")

# TITLE
st.title("📊 AI Mutual Fund Analysis Platform")

# BANNER IMAGE
st.image("images/mutual_fund.jpg", use_container_width=True)


st.write("""
A Mutual Fund pools money from many investors and invests it into stocks, bonds,
or other financial assets. Professional fund managers manage these investments
to generate returns.
""")

st.divider()

# TYPES OF FUNDS
st.header("Types of Mutual Funds")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Equity Funds")
    st.write("Invest mainly in stocks. Higher return but higher risk.")

with col2:
    st.markdown("### 🏦 Debt Funds")
    st.write("Invest in bonds and government securities. Lower risk.")

with col3:
    st.markdown("### ⚖ Hybrid Funds")
    st.write("Combination of equity and debt investments.")

st.divider()

# BENEFITS SECTION
st.header("Why Invest in Mutual Funds?")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Diversification", "✔")

with c2:
    st.metric("Professional Management", "✔")

with c3:
    st.metric("Long-Term Growth", "✔")

with c4:
    st.metric("Easy SIP Investment", "✔")

st.divider()

# PLATFORM FEATURES
st.header("Platform Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Fund Analysis")
    st.write("Analyze fund NAV trends, returns, and risk levels.")

    st.markdown("### 🤖 NAV Prediction")
    st.write("AI predicts future NAV for the next 5 years.")

with col2:
    st.markdown("### 💰 Investment Planner")
    st.write("Calculate SIP and future investment value.")

    st.markdown("### 🧠 Fund Recommendation")
    st.write("AI suggests the best funds based on risk and returns.")

st.success("Use the sidebar to explore fund analysis and AI predictions.")