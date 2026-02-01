import pandas as pd

path = "data/raw/financials.csv"
df = pd.read_csv(path)

print("Rows loaded:", len(df))
print(df.head())
