import streamlit as st
import pandas as pd
import numpy as np

from src.ppv_engine import compute_ppv_impact
from src.time_analysis import add_time_features, monthly_analysis, customer_analysis

st.set_page_config(layout="wide")

st.title("📊 MarginSight AI")
st.subheader("PPV Impact & Time-Based Margin Intelligence")

# -----------------------------
# DEMO DATA
# -----------------------------
def generate_demo_data(n=200):
    np.random.seed(42)

    customers = [f"C{i:03}" for i in range(1, 51)]
    skus = ["A100", "B200", "C300"]

    df = pd.DataFrame({
        "customer_id": np.random.choice(customers, n),
        "sku": np.random.choice(skus, n),
        "order_date": pd.date_range(start="2026-01-01", periods=n, freq="D"),
        "selling_price": np.random.uniform(80, 150, n),
        "standard_cost": np.random.uniform(30, 70, n),
        "cogs": np.random.uniform(5, 20, n),
        "ppv": np.random.uniform(5, 25, n)
    })

    return df

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.title("⚙️ Controls")

data_mode = st.sidebar.radio(
    "Select Data Mode",
    ["Demo Dataset", "Upload Your Data"]
)

# -----------------------------
# Load Data
# -----------------------------
if data_mode == "Demo Dataset":
    df = generate_demo_data(200)
    st.sidebar.success("Using demo dataset ✅")

else:
    file = st.sidebar.file_uploader("Upload your dataset (CSV)")

    if not file:
        st.warning("Please upload a dataset")
        st.stop()

    df = pd.read_csv(file)
    st.sidebar.success("Custom data loaded ✅")

# -----------------------------
# Data Preview
# -----------------------------
st.markdown("### 🧪 Dataset Preview")

with st.expander("View Raw Data"):
    st.dataframe(df.head(50), use_container_width=True)

# -----------------------------
# Filters
# -----------------------------
st.sidebar.markdown("### 🔍 Filters")

selected_customer = st.sidebar.multiselect(
    "Select Customer",
    options=df["customer_id"].unique(),
    default=df["customer_id"].unique()[:5]
)

selected_sku = st.sidebar.multiselect(
    "Select SKU",
    options=df["sku"].unique(),
    default=df["sku"].unique()
)

df = df[
    (df["customer_id"].isin(selected_customer)) &
    (df["sku"].isin(selected_sku))
]

# -----------------------------
# Simulation Control
# -----------------------------
ppv_adjustment = st.sidebar.slider(
    "Simulate PPV Increase (%)",
    0, 50, 0
)

df["ppv"] = df["ppv"] + (df["standard_cost"] * ppv_adjustment / 100)

# -----------------------------
# Processing
# -----------------------------
df = compute_ppv_impact(df)
df = add_time_features(df)

monthly_df = monthly_analysis(df)
customer_df = customer_analysis(df)

# Convert % for display
df["margin_loss_percent"] = df["margin_loss_percent"] * 100

# -----------------------------
# Summary
# -----------------------------
st.markdown("""
### 📊 What this shows:
- Margin impact due to purchase price variation (PPV)
- Time-based margin erosion (monthly trends)
- Customer-level profitability impact
""")

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Margin Loss", round(df["margin_loss"].sum(), 2))
col2.metric("Avg Loss %", round(df["margin_loss_percent"].mean(), 2))
col3.metric("Worst Customer Loss", round(customer_df["margin_loss"].max(), 2))

# -----------------------------
# Charts
# -----------------------------
st.markdown("### 📈 Monthly Margin Loss Trend")
st.line_chart(monthly_df.set_index("month")["margin_loss"])

st.markdown("### 📊 Margin Comparison")
st.line_chart(monthly_df.set_index("month")[["current_margin", "new_margin"]])

st.markdown("### 👤 Top Customers by Margin Loss")
st.bar_chart(
    customer_df.sort_values(by="margin_loss", ascending=False)
    .head(10)
    .set_index("customer_id")
)

# -----------------------------
# Distribution
# -----------------------------
st.markdown("### 📊 Margin Loss Distribution")
st.bar_chart(df["margin_loss"])

# -----------------------------
# Top Orders
# -----------------------------
st.markdown("### 🔴 Top Margin Loss Orders")

top_orders = df.sort_values(by="margin_loss", ascending=False).head(10)

st.dataframe(
    top_orders[[
        "customer_id",
        "sku",
        "margin_loss",
        "margin_loss_percent"
    ]],
    use_container_width=True
)

# -----------------------------
# Table
# -----------------------------
st.markdown("### 📋 Order-Level Analysis")

st.dataframe(
    df[[
        "customer_id",
        "sku",
        "month",
        "current_margin",
        "new_margin",
        "margin_loss",
        "margin_loss_percent"
    ]].sort_values(by="margin_loss", ascending=False),
    use_container_width=True
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built by Rutwik Satish | MarginSight AI")