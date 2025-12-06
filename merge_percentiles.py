import pandas as pd

# Load existing categorized data (with 3-year percentiles)
cat_df = pd.read_csv('categorized_indices.csv')

# Load new 4-year and 5-year percentiles
new_df = pd.read_csv('percentiles_4yr_5yr.csv')

# Merge the data
merged_df = cat_df.merge(
    new_df[['Short_Name', 'Profit_4yr_%', 'Profit_5yr_%', 'Percentile_4yr', 'Percentile_5yr']], 
    on='Short_Name', 
    how='left'
)

# Reorder columns for clarity
column_order = [
    'Category', 'Short_Name', 'Full_Name',
    'Percentile', 'Profit_3yr_%',
    'Percentile_4yr', 'Profit_4yr_%',
    'Percentile_5yr', 'Profit_5yr_%'
]

merged_df = merged_df[column_order]

# Save updated file
merged_df.to_csv('categorized_indices_updated.csv', index=False)

print("✓ Merged 3-year, 4-year, and 5-year data")
print(f"✓ Saved to categorized_indices_updated.csv")
print()

# Show sample
print("Sample data (first 5 indices):")
print(merged_df.head().to_string())
