import pandas as pd

# Load clean data
df = pd.read_csv("data/processed/financials_clean.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort values
df = df.sort_values(["department", "date"])

# --- Financial KPIs ---

# Gross margin
df["gross_margin"] = df["profit"] / df["revenue"]

# Cost ratios
df["payroll_ratio"] = df["payroll_cost"] / df["revenue"]
df["operating_cost_ratio"] = df["operating_cost"] / df["revenue"]

# Month-over-month variance
df["revenue_mom_change"] = df.groupby("department")["revenue"].pct_change()
df["profit_mom_change"] = df.groupby("department")["profit"].pct_change()

# Save output
df.to_csv("data/processed/financials_kpi.csv", index=False)

print("Financial KPIs generated")
