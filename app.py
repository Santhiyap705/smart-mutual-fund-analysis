import streamlit as st

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Smart Mutual Fund Analysis Platform",
    layout="wide"
)

# -----------------------------------------------------
# MAIN LANDING PAGE
# -----------------------------------------------------

st.title("💡 Smart Mutual Fund Analysis & Recommendation Platform")



st.markdown("""
### 📊 Welcome to AI-Based Mutual Fund Platform

This platform helps you to:

- 📊 Analyze mutual fund performance  
- 🤖 Predict future NAV using AI  
- 💰 Plan your SIP investments  
- 🧠 Get smart fund recommendations  

---




### 📘 About

A **Mutual Fund** pools money from multiple investors and invests in stocks, bonds, or other financial assets.  

This system uses **data analysis + AI techniques** to help investors make better decisions.
""")

st.success("👉 Select a module from the sidebar to start exploring!")