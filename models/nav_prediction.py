from prophet import Prophet
import pandas as pd

def predict_nav(nav_df, years=5):

    # rename columns for Prophet
    df = nav_df.rename(columns={"date": "ds", "nav": "y"})

    # safety: remove invalid data
    df = df.dropna()

    # model
    model = Prophet()
    model.fit(df)

    # ✅ 5 years = 365 * years
    future = model.make_future_dataframe(periods=365 * years)

    forecast = model.predict(future)

    return forecast
