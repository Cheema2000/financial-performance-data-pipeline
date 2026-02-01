import pandas as pd

df = pd.read_csv("data/raw/financials.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop rows with missing critical values
df = df.dropna(subset=["date", "department"])

# Convert numeric columns
for col in ["revenue", "operating_cost", "payroll_cost"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove invalid records
df = df[
    (df["revenue"] >= 0) &
    (df["operating_cost"] >= 0) &
    (df["payroll_cost"] >= 0)
]

# Create profit metric
df["profit"] = df["revenue"] - (df["operating_cost"] + df["payroll_cost"])

# Save clean dataset
df.to_csv("data/processed/financials_clean.csv", index=False)

print("Clean dataset created:", len(df), "rows")
