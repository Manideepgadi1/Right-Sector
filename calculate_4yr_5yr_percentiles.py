import pandas as pd
import numpy as np

# Load the raw data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
df = df.sort_values('DATE')

print(f"Data range: {df['DATE'].min()} to {df['DATE'].max()}")
print(f"Total rows: {len(df)}")
print()

# Load categorized indices to get the mapping
cat_df = pd.read_csv('categorized_indices.csv')

results = []

# Calculate for each index
for _, row in cat_df.iterrows():
    short_name = row['Short_Name']
    full_name = row['Full_Name']
    category = row['Category']
    
    # Find matching column in raw data
    col_name = None
    for col in df.columns:
        if col == short_name or col == full_name:
            col_name = col
            break
    
    if col_name is None:
        print(f"Warning: Could not find column for {short_name}")
        continue
    
    # Get price series
    prices = df[col_name].dropna()
    
    if len(prices) < 2:
        print(f"Warning: Not enough data for {short_name}")
        continue
    
    current_price = prices.iloc[-1]
    
    # Calculate 4-year profit
    # 4 years = ~1008 trading days (252 days per year * 4)
    profit_4yr = None
    if len(prices) >= 1008:
        price_4yr_ago = prices.iloc[-1008]
        profit_4yr = ((current_price - price_4yr_ago) / price_4yr_ago) * 100
    else:
        print(f"Warning: Not enough data for 4-year calculation for {short_name} (only {len(prices)} days)")
    
    # Calculate 5-year profit
    # 5 years = ~1260 trading days (252 days per year * 5)
    profit_5yr = None
    if len(prices) >= 1260:
        price_5yr_ago = prices.iloc[-1260]
        profit_5yr = ((current_price - price_5yr_ago) / price_5yr_ago) * 100
    else:
        print(f"Warning: Not enough data for 5-year calculation for {short_name} (only {len(prices)} days)")
    
    results.append({
        'Category': category,
        'Short_Name': short_name,
        'Full_Name': full_name,
        'Profit_4yr_%': profit_4yr,
        'Profit_5yr_%': profit_5yr
    })

# Create DataFrame
results_df = pd.DataFrame(results)

# Calculate rankings and percentiles for 4-year profit
valid_4yr = results_df[results_df['Profit_4yr_%'].notna()].copy()
if len(valid_4yr) > 0:
    valid_4yr['Rank_4yr'] = valid_4yr['Profit_4yr_%'].rank(method='min')
    valid_4yr['Percentile_4yr'] = (valid_4yr['Rank_4yr'] - 1) / (len(valid_4yr) - 1)
    results_df = results_df.merge(
        valid_4yr[['Short_Name', 'Rank_4yr', 'Percentile_4yr']], 
        on='Short_Name', 
        how='left'
    )
else:
    results_df['Rank_4yr'] = None
    results_df['Percentile_4yr'] = None

# Calculate rankings and percentiles for 5-year profit
valid_5yr = results_df[results_df['Profit_5yr_%'].notna()].copy()
if len(valid_5yr) > 0:
    valid_5yr['Rank_5yr'] = valid_5yr['Profit_5yr_%'].rank(method='min')
    valid_5yr['Percentile_5yr'] = (valid_5yr['Rank_5yr'] - 1) / (len(valid_5yr) - 1)
    results_df = results_df.merge(
        valid_5yr[['Short_Name', 'Rank_5yr', 'Percentile_5yr']], 
        on='Short_Name', 
        how='left'
    )
else:
    results_df['Rank_5yr'] = None
    results_df['Percentile_5yr'] = None

# Save to CSV
output_file = 'percentiles_4yr_5yr.csv'
results_df.to_csv(output_file, index=False)

print(f"✓ Calculated 4-year and 5-year percentiles for {len(results_df)} indices")
print(f"✓ 4-year data available for: {valid_4yr.shape[0]} indices")
print(f"✓ 5-year data available for: {valid_5yr.shape[0]} indices")
print(f"✓ Saved to {output_file}")
print()

# Show summary statistics
print("4-Year Profit Summary:")
print(f"  Min: {results_df['Profit_4yr_%'].min():.2f}%")
print(f"  Max: {results_df['Profit_4yr_%'].max():.2f}%")
print(f"  Mean: {results_df['Profit_4yr_%'].mean():.2f}%")
print(f"  Median: {results_df['Profit_4yr_%'].median():.2f}%")
print()

print("5-Year Profit Summary:")
print(f"  Min: {results_df['Profit_5yr_%'].min():.2f}%")
print(f"  Max: {results_df['Profit_5yr_%'].max():.2f}%")
print(f"  Mean: {results_df['Profit_5yr_%'].mean():.2f}%")
print(f"  Median: {results_df['Profit_5yr_%'].median():.2f}%")
print()

# Show top 10 by 4-year performance
print("Top 10 by 4-Year Profit:")
top_4yr = results_df.nlargest(10, 'Profit_4yr_%')[['Short_Name', 'Profit_4yr_%', 'Percentile_4yr']]
for idx, row in top_4yr.iterrows():
    print(f"  {row['Short_Name']:<20} {row['Profit_4yr_%']:>8.2f}%  Percentile: {row['Percentile_4yr']:.3f}")
print()

# Show top 10 by 5-year performance
print("Top 10 by 5-Year Profit:")
top_5yr = results_df.nlargest(10, 'Profit_5yr_%')[['Short_Name', 'Profit_5yr_%', 'Percentile_5yr']]
for idx, row in top_5yr.iterrows():
    print(f"  {row['Short_Name']:<20} {row['Profit_5yr_%']:>8.2f}%  Percentile: {row['Percentile_5yr']:.3f}")
