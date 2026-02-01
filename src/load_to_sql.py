import pandas as pd
import sqlite3

conn = sqlite3.connect("financials.db")

financials = pd.read_csv("data/processed/financials_kpi.csv")
summary = pd.read_csv("data/processed/department_summary.csv")

financials.to_sql("financials", conn, if_exists="replace", index=False)
summary.to_sql("department_summary", conn, if_exists="replace", index=False)

conn.close()

print("Data successfully loaded into SQLite database")
