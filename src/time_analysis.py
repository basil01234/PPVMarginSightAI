import pandas as pd

def add_time_features(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["quarter"] = df["order_date"].dt.to_period("Q").astype(str)
    return df


def monthly_analysis(df):
    return df.groupby("month").agg({
        "current_margin": "sum",
        "new_margin": "sum",
        "margin_loss": "sum"
    }).reset_index()


def customer_analysis(df):
    return df.groupby("customer_id")["margin_loss"].sum().reset_index()
