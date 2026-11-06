from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import kurtosis, skew


# Load the dataset relative to this script so it works from any directory.
csv_path = Path(__file__).resolve().parent / "vertex_sales_inventory.csv"
df = pd.read_csv(csv_path)

# Display the first and last five rows.
print("First 5 rows:")
print(df.head(5).to_string(index=False))
print("\nLast 5 rows:")
print(df.tail(5).to_string(index=False))

# DataFrame structure, types, and nulls.
df.info()

# Duplicate rows
duplicate_count = df.duplicated().sum()
duplicate_percentage = (duplicate_count / len(df)) * 100

print(f"\nDuplicate rows: {duplicate_count}")
print(f"Duplicate percentage: {duplicate_percentage:.2f}%")

if duplicate_percentage > 5:
    print("\nDuplicate report: More than 5% of the rows are duplicated.")
    print(df[df.duplicated(keep=False)].head(10).to_string(index=False))
else:
    df = df.drop_duplicates()
    print("Duplicates dropped because they represent 5% or less of the data.")

# Null values by column
null_percentage = (df.isna().sum() / len(df)) * 100
print("\nNull percentage by variable:")
print(null_percentage.round(2).to_string())

total_nulls = df.isna().sum().sum()
print(f"\nTotal null values in the DataFrame: {total_nulls}")

columns_above_threshold = null_percentage[null_percentage > 10]
if not columns_above_threshold.empty:
    print("\nNull report: One or more variables exceed 10% null values.")
    print(columns_above_threshold.round(2).to_string() + "%")
else:
    df = df.dropna()
    print("Null rows dropped because no variable exceeds the 10% null threshold.")

# Keep the duplicate and null cleaning used for outlier analysis.
df = df.drop_duplicates().dropna()

# IQR outlier analysis for numeric variables.
numeric_columns = df.select_dtypes(include="number").columns
outlier_mask = pd.Series(False, index=df.index)

print("\nIQR outlier report:")
for column in numeric_columns:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    column_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    outlier_count = int(column_mask.sum())
    outlier_percentage = (outlier_count / len(df)) * 100

    print(
        f"{column}: {outlier_count} outliers "
        f"({outlier_percentage:.2f}% of rows)"
    )
    outlier_mask |= column_mask

total_outliers = int(outlier_mask.sum())
total_outlier_percentage = (total_outliers / len(df)) * 100
print(
    f"\nTotal rows with at least one outlier: {total_outliers} "
    f"({total_outlier_percentage:.2f}% of rows)"
)

# Skewness and kurtosis before filtering outlier rows.
print("\nSkewness and kurtosis by numeric variable:")
for column in numeric_columns:
    values = df[column].dropna()
    print(
        f"{column}: Skewness={skew(values):.2f}, "
        f"Kurtosis={kurtosis(values, fisher=True):.2f}"
    )

df = df.loc[~outlier_mask]
print(df["promotion_active"].unique())
print(df["is_holiday"].unique())
print(df["stockout_flag"].unique())