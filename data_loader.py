import pandas as pd
import streamlit as st

# -----------------------------
# LOAD FULL CSV DATA
# -----------------------------
@st.cache_data(ttl=3600)
def load_data():

    try:
        df = pd.read_csv("schemes.csv")

        # clean column names
        df.columns = df.columns.str.strip()

        # convert types
        df["date"] = pd.to_datetime(df["date"])
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

        # remove invalid rows
        df = df.dropna()

        return df

    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return pd.DataFrame()


# -----------------------------
# LOAD SCHEMES
# -----------------------------
@st.cache_data(ttl=3600)
def load_schemes():

    df = load_data()

    if df.empty:
        st.warning("⚠ No data found in CSV")
        return pd.DataFrame()

    # remove duplicates (important)
    schemes = df[["SchemeCode", "Scheme Name", "category"]].drop_duplicates()

    return schemes


# -----------------------------
# LOAD NAV DATA
# -----------------------------
@st.cache_data(ttl=3600)
def load_nav(code):

    df = load_data()

    nav_df = df[df["SchemeCode"] == code].copy()

    if nav_df.empty:
        return nav_df

    # sort by date
    nav_df = nav_df.sort_values("date")

    # 🔥 OPTIONAL: limit last 5 years (fast)
    nav_df = nav_df[
        nav_df["date"] > nav_df["date"].max() - pd.DateOffset(years=5)
    ]

    return nav_df