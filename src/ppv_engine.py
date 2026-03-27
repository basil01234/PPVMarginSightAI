def compute_ppv_impact(df):

    df["current_margin"] = df["selling_price"] - (
        df["standard_cost"] + df["cogs"]
    )

    df["new_cost"] = df["standard_cost"] + df["ppv"]

    df["new_margin"] = df["selling_price"] - (
        df["new_cost"] + df["cogs"]
    )

    df["margin_loss"] = df["current_margin"] - df["new_margin"]

    df["margin_loss_percent"] = df["margin_loss"] / df["selling_price"]

    return df
