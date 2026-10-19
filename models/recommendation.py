import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def recommend_funds(df):

    scaler = MinMaxScaler()

    df[["return_score","risk_score","sharpe_score"]] = scaler.fit_transform(
        df[["return","risk","sharpe"]]
    )

    # final ranking score
    df["final_score"] = (
        df["return_score"] +
        df["sharpe_score"] -
        df["risk_score"]
    )

    recommended = df.sort_values(
        "final_score",
        ascending=False
    )

    return recommended.head(5)
