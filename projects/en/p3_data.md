# Project 3 — Sales Data Analysis

Analyze sales data using pandas and matplotlib to extract insights.

## Overview:
Analyze monthly sales data from a CSV file to find trends, totals, and create visualizations.

## Data File:
`sales.csv` with columns: date, product, category, price, quantity, city

Example data:
```csv
date,product,category,price,quantity,city
1403/01/05,Widget Pro,Widgets,850000,2,Tehran
1403/01/07,Gadget Mini,Gadgets,320000,5,Shiraz
1403/01/12,Gadget Max,Gadgets,45000,20,Mashhad
1403/02/01,Widget Pro,Widgets,3200000,1,Tehran
```

## Tasks:

### 1. Load & Inspect
- Load `sales.csv` using pandas with UTF-8 encoding
- Display first 5 rows with `.head()`
- Show data info with `.info()`
- Check for missing values with `.isna().sum()`
- Create a `total` column: `total = price * quantity`
- Extract `month` from the date column

### 2. Analysis
- Show total sales by category, sorted descending
- Show average sales by city
- Pivot table: categories as rows, months as columns, values = total sales

### 3. Visualization
- Bar chart: total sales by category
- Save the chart as `sales_by_category.png` (150 DPI)
- Show category totals in a table

### 4. Advanced (Optional)
- Add subplots (multiple charts in one figure)
- Handle missing values (drop or fill)
- Linear regression with scikit-learn to predict sales trend

## Example Code Structure:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("sales.csv", encoding="utf-8")

# Create total column
df["total"] = df["price"] * df["quantity"]

# Convert date and extract month
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month

# Group by category
by_category = df.groupby("category")["total"].sum().sort_values(ascending=False)

# Bar chart
plt.figure(figsize=(10, 5))
by_category.plot(kind="bar")
plt.title("Total Sales by Category")
plt.ylabel("Total Sales (Currency)")
plt.tight_layout()
plt.savefig("sales_by_category.png", dpi=150)
plt.show()
```

## Checklist:
- [ ] Load CSV and inspect data
- [ ] Create `total` column from price and quantity
- [ ] Extract month from date column
- [ ] Group by category and show totals (sorted)
- [ ] Create and save bar chart as PNG
- [ ] Group by city and show averages
- [ ] Create pivot table by category and month
- [ ] (Optional) Add subplots or advanced analysis