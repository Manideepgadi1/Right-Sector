import pandas as pd
import numpy as np
import json

# Load the raw data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
df = df.sort_values('DATE')

# Load categorized indices to get the mapping
cat_df = pd.read_csv('categorized_indices.csv')

# Create a mapping of short names to column names
name_mapping = {}
for _, row in cat_df.iterrows():
    short_name = row['Short_Name']
    full_name = row['Full_Name']
    
    # Find matching column
    for col in df.columns:
        if col == short_name or col == full_name:
            name_mapping[short_name] = col
            break

print(f"Found {len(name_mapping)} indices in the data")

# Calculate correlation matrix for all indices
price_data = {}
for short_name, col_name in name_mapping.items():
    if col_name in df.columns:
        # Get price series and calculate returns
        prices = df[col_name].dropna()
        if len(prices) > 1:
            # Use last 252 days (1 year) or all available
            if len(prices) > 252:
                prices = prices.iloc[-252:]
            price_data[short_name] = prices.values

# Create DataFrame for correlation calculation
price_df = pd.DataFrame()
for name, prices in price_data.items():
    if len(prices) > 0:
        # Align all series to the same length (use minimum length)
        price_df[name] = pd.Series(prices)

# Fill NaN with forward fill then backward fill
price_df = price_df.ffill().bfill()

# Calculate returns (percentage change)
returns_df = price_df.pct_change().dropna()

# Calculate correlation matrix
corr_matrix = returns_df.corr()

# Convert to dictionary
corr_dict = {}
for idx in corr_matrix.index:
    corr_dict[idx] = {}
    for col in corr_matrix.columns:
        value = corr_matrix.loc[idx, col]
        # Handle NaN values
        if pd.isna(value):
            corr_dict[idx][col] = 0.0
        else:
            # Cast to float explicitly to satisfy type checker
            corr_dict[idx][col] = round(float(float(value)), 3)

# Save to JSON
with open('correlation_matrix.json', 'w') as f:
    json.dump(corr_dict, f, indent=2)

print(f"✓ Generated correlation matrix for {len(corr_dict)} indices")
print(f"✓ Saved to correlation_matrix.json")

# Show sample correlations for NREALTY
if 'NREALTY' in corr_dict:
    print("\nSample correlations (NREALTY):")
    sample_indices = list(corr_dict['NREALTY'].keys())[:5]
    for idx in sample_indices:
        print(f"  NREALTY vs {idx}: {corr_dict['NREALTY'][idx]}")
