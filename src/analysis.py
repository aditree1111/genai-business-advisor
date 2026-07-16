"""
#Read the csv file
df = pd.read_csv("data/SampleSuperstore.csv")

#show the first 5 row
print("first 5 rows")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumns names")
print(df.columns)

print("\nData types")
print(df.dtypes) 
print("\nMissing values")
print(df.isnull().sum())

print("\nTotal sales")
total_sales = df['Sales'].sum()
print(total_sales)
 
print("\nTotal profit")
print(df["Profit"].sum())

print("\nTotal Orders")
print(df["Quantity"].nunique())

print("\nSales by Category")
sales_by_category = df.groupby("Category")["Sales"].sum()
print(sales_by_category)

print("\nProfit by Category")
profit_by_category = df.groupby("Category")["Profit"].sum()
print(profit_by_category)

print("\nSales by Region")
sales_by_region = df.groupby("Region")["Sales"].sum()
print(sales_by_region)

print("\nProfit by Region")
profit_by_region = df.groupby("Region")["Profit"].sum()
print(profit_by_region)

print("\nTop 10 States by Sales")
top_states = df.groupby("State")["Sales"].sum().sort_values(ascending=False)
print(top_states.head(10))

print("\nTop Categories by Profit")
top_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print(top_profit) 

print("\nTop 10 Products by Sales")
top_products = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)
print(top_products.head(10))


print("\nTop 10 Sub-Categories by Profit")
top_profit = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)
print(top_profit.head(10))

print("\nLoss Making Sub-Categories")
loss_products = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values()
)
print(loss_products.head())

print("\nSales by Customer Segment")
segment_sales = (
    df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)
print(segment_sales)

print("\nAverage Discount")
print(df["Discount"].mean())

print("\nAverage Profit")
print(df["Profit"].mean())
"""

import pandas as pd

# Load dataset
df = pd.read_csv("data/SampleSuperstore.csv")


def calculate_kpis(df):
    print("\n===== BUSINESS KPIs =====")
    print(f"Total Sales: {df['Sales'].sum():,.2f}")
    print(f"Total Profit: {df['Profit'].sum():,.2f}")
    print(f"Total Quantity Sold: {df['Quantity'].sum()}")
    print(f"Average Profit: {df['Profit'].mean():.2f}")


def category_analysis(df):
    print("\n===== SALES BY CATEGORY =====")
    print(df.groupby("Category")["Sales"].sum())

    print("\n===== PROFIT BY CATEGORY =====")
    print(df.groupby("Category")["Profit"].sum())


def region_analysis(df):
    print("\n===== SALES BY REGION =====")
    print(df.groupby("Region")["Sales"].sum())

    print("\n===== PROFIT BY REGION =====")
    print(df.groupby("Region")["Profit"].sum())


# Run all analyses
calculate_kpis(df)
category_analysis(df)
region_analysis(df)