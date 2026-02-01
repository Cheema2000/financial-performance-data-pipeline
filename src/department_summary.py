import pandas as pd

df = pd.read_csv("data/processed/financials_kpi.csv")

summary = (
    df.groupby("department")
    .agg(
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_margin=("gross_margin", "mean"),
        avg_payroll_ratio=("payroll_ratio", "mean")
    )
    .reset_index()
)

summary.to_csv("data/processed/department_summary.csv", index=False)

print("Department-level summary created")
