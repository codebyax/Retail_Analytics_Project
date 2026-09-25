import pandas as pd
import numpy as np


filepath ='C:\\Users\\chanc\\Desktop\\NPower_Docs\\DataAnalysis_Presentation\\18100245-eng\\18100245.csv'
df = pd.read_csv(filepath, header=0) 

print(df.head())

df.replace("?", np.nan, inplace = True)
print(df.head(5))

# Evaluating for Missing Data
missing_data = df.isnull()
print(missing_data.head(5))

for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")   


df.drop(columns=["SYMBOL", "TERMINATED"], inplace=True)
print(df.head(5))

avg_value=df["VALUE"].astype(float).mean(axis=0)
df["VALUE"].replace(np.nan, avg_value, inplace=True)
print("Average VALUE:", avg_value)

# converting datatypes
df["REF_DATE"] = pd.to_datetime(df["REF_DATE"])
df["GEO"] = df["GEO"].astype('category')
df["DGUID"] = df["DGUID"].astype('object')
df["Products"] = df["Products"].astype('category')
df["UOM"] = df["UOM"].astype('object')
df["SCALAR_FACTOR"] = df["SCALAR_FACTOR"].astype('object')
df["VECTOR"] = df["VECTOR"].astype('object')


print(df.dtypes)
print(df.info())
df_norm = df.copy()

# keep only numeric columns (for normalization on value column)
df["VALUE_norm"] = (df["VALUE"] - df["VALUE"].min()) / (df["VALUE"].max() - df["VALUE"].min())   

print(df.head(5))

# create 3 bins for VALUE
bins = np.linspace(df["VALUE"].min(), df["VALUE"].max(), 4)

group_names = ['Low', 'Medium', 'High']
df["VALUE_bin"] = pd.cut(df["VALUE"], bins, labels=group_names, include_lowest=True)

print(df[["VALUE", "VALUE_bin"]].head())

# indicator for data trend analysis
# 1. Price Change Indicator:

df = df.sort_values(["Products", "GEO", "REF_DATE"])

df["price_change"] = df.groupby(["Products", "GEO"])["VALUE"].diff()

df["price_pct_change"] = (
    df.groupby(["Products", "GEO"])["VALUE"]
      .pct_change()
)
# 2. Moving Average (trend):
df["MA_3"] = (
    df.groupby(["Products", "GEO"])["VALUE"]
      .transform(lambda x: x.rolling(3).mean())
)

df["MA_7"] = (
    df.groupby(["Products", "GEO"])["VALUE"]
      .transform(lambda x: x.rolling(7).mean())
)

# 3. Binary Up/Down Indicator:

df["price_up"] = (
    df.groupby(["Products", "GEO"])["VALUE"]
      .diff()
      .gt(0)
      .astype("Int64")
)

# 4. Category Indicator:
df["price_category"] = pd.cut(df["VALUE"], bins=3, labels=["Low", "Medium", "High"])

# 5. Date-based Indicators:
df["month"] = pd.to_datetime(df["REF_DATE"]).dt.month
df["year"] = pd.to_datetime(df["REF_DATE"]).dt.year
df["quarter"] = pd.to_datetime(df["REF_DATE"]).dt.quarter

print(df.head(5))
# Save the cleaned DataFrame to a new CSV file
df.to_csv('C:\\Users\\chanc\\Desktop\\NPower_Docs\\DataAnalysis_Presentation\\18100245_cleaned.csv', index=False)