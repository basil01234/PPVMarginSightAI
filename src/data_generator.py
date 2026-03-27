import pandas as pd
import numpy as np

def generate_data(n=200):
    np.random.seed(42)

    customers = [f"C{i:03}" for i in range(n)]
    skus = ["A100", "B200", "C300"]

    df = pd.DataFrame({
        "customer_id": np.random.choice(customers, n),
        "sku": np.random.choice(skus, n),
        "order_date": pd.date_range(start="2026-01-01", periods=n, freq="D"),
        "selling_price": np.random.uniform(80, 150, n),
        "standard_cost": np.random.uniform(30, 70, n),
        "cogs": np.random.uniform(5, 20, n),
        "ppv": np.random.uniform(0, 25, n)  # tariff variation
    })
    print(df)
    return df