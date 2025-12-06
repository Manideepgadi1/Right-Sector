import pandas as pd
import numpy as np
import json

# Load the raw data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
df = df.sort_values('DATE')

# Load categorized indices with updated percentiles
cat_df = pd.read_csv('categorized_indices_updated.csv')

# Prepare basket data
basket_data = {}

for _, row in cat_df.iterrows():
    short_name = row['Short_Name']
    full_name = row['Full_Name']
    
    # Find matching column in raw data (try both short name and full name)
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
    
    # Current price (latest)
    current_price = prices.iloc[-1]
    
    # Calculate various metrics
    # 1. % Change (1 year)
    if len(prices) >= 252:  # ~1 year of trading days
        price_1yr_ago = prices.iloc[-252]
        pct_change_1yr = ((current_price - price_1yr_ago) / price_1yr_ago) * 100
    else:
        pct_change_1yr = ((current_price - prices.iloc[0]) / prices.iloc[0]) * 100
    
    # 2. Up % - Upside potential from recent low (52 week low)
    if len(prices) >= 252:
        recent_prices = prices.iloc[-252:]
    else:
        recent_prices = prices
    
    low_52week = recent_prices.min()
    upside_from_low = ((current_price - low_52week) / low_52week) * 100
    
    # 3. Low % - Percentage below 52 week high
    high_52week = recent_prices.max()
    low_pct = ((current_price - high_52week) / high_52week) * 100
    
    # 4. High % - Percentage above 52 week low
    high_pct = ((current_price - low_52week) / low_52week) * 100
    
    # 5. Risk - Distance from 52 week high (negative = below high)
    distance_from_high = ((current_price - high_52week) / high_52week) * 100
    
    basket_data[short_name] = {
        'full_name': full_name,
        'pct_change_1yr': round(pct_change_1yr, 2),
        'upside_from_low': round(upside_from_low, 2),
        'low_pct': round(low_pct, 2),  # % below 52w high
        'high_pct': round(high_pct, 2),  # % above 52w low
        'percentile_3yr': round(row['Percentile'], 3),
        'percentile_4yr': round(row['Percentile_4yr'], 3),
        'percentile_5yr': round(row['Percentile_5yr'], 3)
    }

# Save to JSON file
with open('basket_data.json', 'w') as f:
    json.dump(basket_data, f, indent=2)

print(f"✓ Generated basket data for {len(basket_data)} indices")
print(f"✓ Saved to basket_data.json")

# Show sample
print("\nSample data (NREALTY):")
if 'NREALTY' in basket_data:
    sample = basket_data['NREALTY']
    for key, value in sample.items():
        print(f"  {key}: {value}")
