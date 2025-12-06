import pandas as pd
import numpy as np

# Load the CSV data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
df = df.sort_values('DATE').reset_index(drop=True)

print("="*100)
print("CALCULATING 3-YEAR PROFIT AND PERCENTILE RANKS")
print("="*100)
print(f"Latest date: {df['DATE'].iloc[-1]}")
print(f"Total rows: {len(df)}")
print()

# Index mapping from sample image
index_mapping = {
    'N50': 'NIFTY 50',
    'NN50': 'NIFTY NEXT 50',
    'N100': 'NIFTY 100',
    'N200': 'NIFTY 200',
    'NTOTLM': 'Nifty Total Market',
    'N500': 'NIFTY 500',
    'NMID150': 'NIFTY MIDCAP 150',
    'MMCSEL': 'Nifty Midcap Select',
    'NMC100': 'NIFTY Midcap 100',
    'NSC100': 'NIFTY SMALLCAP 100',
    'NMICRO': 'NIFTY MICROCAP 250',
}

expected_values = {
    'N50': 0.48,
    'NN50': 0.57,
    'N100': 0.48,
    'N200': 0.57,
    'NTOTLM': 0.57,
    'N500': 0.57,
    'NMID150': 0.6,
    'MMCSEL': 0.76,
    'NMC100': 0.71,
    'NSC100': 0.79,
    'NMICRO': 0.5,
}

all_indices = [col for col in df.columns if col != 'DATE']

# Calculate 3-year profits (returns) for all indices
lookback_days = 756  # Approximately 3 years of trading days (252 * 3)

print("="*100)
print("STEP 1: Calculate 3-Year Profit (Return) for Each Index")
print("="*100)

profits_3yr = {}
profit_details = []

for col in all_indices:
    current_price = df[col].iloc[-1]
    price_3yr_ago = df[col].iloc[-lookback_days] if len(df) >= lookback_days else None
    
    if pd.notna(current_price) and pd.notna(price_3yr_ago) and price_3yr_ago > 0:
        # Calculate absolute profit
        profit_amount = current_price - price_3yr_ago
        
        # Calculate profit percentage (growth rate)
        profit_percentage = (profit_amount / price_3yr_ago) * 100
        
        profits_3yr[col] = profit_percentage
        
        profit_details.append({
            'Index': col,
            'Price_3yr_ago': price_3yr_ago,
            'Current_Price': current_price,
            'Profit_Amount': profit_amount,
            'Profit_Percentage': profit_percentage
        })

# Create DataFrame for easier analysis
profit_df = pd.DataFrame(profit_details)
profit_df = profit_df.sort_values('Profit_Percentage', ascending=False).reset_index(drop=True)

print(f"\nTotal indices analyzed: {len(profits_3yr)}")
print(f"\nTop 10 Profit Performers:")
print(profit_df.head(10)[['Index', 'Profit_Percentage']].to_string(index=False))

print(f"\nBottom 10 Profit Performers:")
print(profit_df.tail(10)[['Index', 'Profit_Percentage']].to_string(index=False))

# STEP 2: Rank all indices by their 3-year profit
print(f"\n{'='*100}")
print("STEP 2: Rank All Indices by 3-Year Profit")
print("="*100)

profits_series = pd.Series(profits_3yr)

# Rank: 1 = lowest profit, N = highest profit
ranks = profits_series.rank(method='average')

print(f"\nRanking statistics:")
print(f"Lowest rank (worst performer): {ranks.min()}")
print(f"Highest rank (best performer): {ranks.max()}")
print(f"Total indices ranked: {len(ranks)}")

# STEP 3: Convert ranks to percentiles (0-1 scale)
print(f"\n{'='*100}")
print("STEP 3: Convert Ranks to Percentiles (0-1 Scale)")
print("="*100)

# Percentile: 0 = worst performer, 1 = best performer
percentiles = profits_series.rank(pct=True)

print(f"\nPercentile statistics:")
print(f"Minimum percentile: {percentiles.min():.4f}")
print(f"Maximum percentile: {percentiles.max():.4f}")
print(f"Mean percentile: {percentiles.mean():.4f}")
print(f"Median percentile: {percentiles.median():.4f}")

# Create comprehensive results DataFrame
results_df = pd.DataFrame({
    'Index': profits_series.index,
    'Profit_3yr_Percentage': profits_series.values,
    'Rank': ranks.values,
    'Percentile': percentiles.values
})

results_df = results_df.sort_values('Rank', ascending=False).reset_index(drop=True)

# Test against expected values
print(f"\n{'='*100}")
print("TESTING AGAINST SAMPLE IMAGE VALUES")
print("="*100)

matches = 0
total = 0
test_results = []

for short_name, expected_val in expected_values.items():
    if short_name in index_mapping:
        col_name = index_mapping[short_name]
        
        if col_name in percentiles:
            percentile = percentiles[col_name]
            profit = profits_3yr[col_name]
            rank = ranks[col_name]
            difference = abs(percentile - expected_val)
            
            total += 1
            if difference < 0.05:
                matches += 1
                match_indicator = "✓✓✓ EXCELLENT"
            elif difference < 0.10:
                match_indicator = "✓✓ GOOD"
            else:
                match_indicator = "✗"
            
            test_results.append({
                'Short_Name': short_name,
                'Index': col_name,
                'Expected': expected_val,
                'Calculated_Percentile': percentile,
                'Profit_3yr_%': profit,
                'Rank': rank,
                'Difference': difference,
                'Match': match_indicator
            })

test_df = pd.DataFrame(test_results)
print("\n" + test_df.to_string(index=False))

if total > 0:
    accuracy = (matches / total) * 100
    print(f"\n{'='*100}")
    print(f"*** ACCURACY: {matches}/{total} = {accuracy:.1f}% ***")
    print(f"{'='*100}")
    
    if accuracy >= 70:
        print("\n🎯 FORMULA FOUND!")
        print("\nFormula:")
        print("1. Calculate 3-year profit: (Current Price - Price 3 years ago) / Price 3 years ago × 100")
        print("2. Rank all indices by their 3-year profit percentage")
        print("3. Convert rank to percentile (0 = worst performer, 1 = best performer)")
    elif accuracy >= 50:
        print("\n⚠️ Partial match - may need refinement")
    else:
        print("\n❌ Low accuracy - formula likely incorrect")

# Save complete results to CSV
output_file = 'profit_percentile_results.csv'
results_df.to_csv(output_file, index=False)
print(f"\n✓ Complete results saved to: {output_file}")

# Display distribution
print(f"\n{'='*100}")
print("PERCENTILE DISTRIBUTION")
print("="*100)

bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ['Very Low (0-0.2)', 'Low (0.2-0.4)', 'Medium (0.4-0.6)', 'High (0.6-0.8)', 'Very High (0.8-1.0)']
percentile_bins = pd.cut(percentiles, bins=bins, labels=labels, include_lowest=True)

distribution = percentile_bins.value_counts().sort_index()
print("\n" + distribution.to_string())

# Show sample indices in each category
print(f"\n{'='*100}")
print("SAMPLE INDICES BY CATEGORY")
print("="*100)

for label in labels:
    indices_in_category = results_df[results_df['Percentile'].between(
        bins[labels.index(label)], 
        bins[labels.index(label) + 1]
    )]['Index'].head(3).tolist()
    
    if indices_in_category:
        print(f"\n{label}:")
        for idx in indices_in_category:
            perc = percentiles[idx]
            profit = profits_3yr[idx]
            print(f"  - {idx}: Percentile={perc:.3f}, Profit={profit:.1f}%")
