import pandas as pd
import numpy as np

# Load the CSV data
df = pd.read_csv('data/Latest_Indices_rawdata_14112025.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y')
df = df.sort_values('DATE').reset_index(drop=True)

print("="*100)
print("CALCULATING 3-YEAR PROFIT AND PERCENTILE RANKS - CATEGORIZED")
print("="*100)
print(f"Latest date: {df['DATE'].iloc[-1]}")
print(f"Total rows: {len(df)}")
print()

# Define categories with their indices
categories = {
    'Broad': {
        'N50': 'NIFTY 50',
        'NN50': 'NIFTY NEXT 50',
        'N100': 'NIFTY 100',
        'N200': 'NIFTY 200',
        'NTOTLM': 'Nifty Total Market',
        'N500': 'NIFTY 500',
        'NMC5025': 'NIFTY500 MULTICAP 50:25:25',
        'N500EQ': 'NIFTY500 EQUAL WEIGHT',
        'NMC150': 'NIFTY MIDCAP 150',
        'NMC50': 'NIFTY MIDCAP 50',
        'NMIDSEL': 'Nifty Midcap Select',
        'NMC100': 'NIFTY Midcap 100',
        'NSC250': 'NIFTY SMALLCAP 250',
        'NSC50': 'NIFTY SMALLCAP 50',
        'NSC100': 'NIFTY SMALLCAP 100',
        'NMICRO': 'NIFTY MICROCAP 250',
        'NLMC250': 'NIFTY LargeMidcap 250',
        'NMSC400': 'NIFTY MIDSMALLCAP 400'
    },
    'Sector': {
        'NAUTO': 'NIFTY AUTO',
        'NBANK': 'NIFTY BANK',
        'NCHEM': 'NIFTY CHEMICALS',
        'NFINSERV': 'NIFTY FINANCIAL SERVICES',
        'NFINS25': 'NIFTY FINANCIAL SERVICES 25/50',
        'NFINSEXB': 'Nifty Financial Services Ex Bank',
        'NFMCG': 'NIFTY FMCG',
        'NHEALTH': 'Nifty HEALTHCARE',
        'NTECH': 'NIFTY IT',
        'NMEDIA': 'NIFTY MEDIA',
        'NMETAL': 'NIFTY METAL',
        'NPHARMA': 'NIFTY PHARMA',
        'NPVTBANK': 'NIFTY PRIVATE BANK',
        'NPSUBANK': 'NIFTY PSU BANK',
        'NREALTY': 'NIFTY REALTY',
        'NCONDUR': 'NIFTY CONSUMER DURABLES',
        'NOILGAS': 'NIFTY OIL AND GAS INDEX',
        'NMSFINS': 'Nifty MidSmall Financial Services',
        'NMSHC': 'Nifty MidSmall Healthcare',
        'NMSITT': 'Nifty MidSmall IT & Telecom'
    },
    'Strategy': {
        'N100EQWT': 'NIFTY 100 EQUAL WEIGHT',
        'N100LV30': 'NIFTY 100 LOW VOLATILITY 30',
        'N5ARB': 'NIFTY ALPHA 50',
        'N200M30': 'NIFTY200 MOMENTUM 30',
        'N200AL30': 'NIFTY200 ALPHA 30',
        'N100AL30': 'NIFTY100 ALPHA 30',
        'NAL50': 'NIFTY ALPHA 50',
        'NALV30': 'NIFTY ALPHA LOW VOLATILITY 30',
        'NAQLV30': 'NIFTY ALPHA QUALITY LOW VOLATILITY 30',
        'NAQVLV30': 'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30',
        'NDIVOP50': 'NIFTY DIVIDEND OPPORTUNITIES 50',
        'NGROW15': 'NIFTY GROWTH SECTORS 15',
        'NHBETA50': 'NIFTY HIGH BETA 50',
        'NLV50': 'NIFTY LOW VOLATILITY 50',
        'NTOP10EW': 'NIFTY TOP 10 EQUAL WEIGHT',
        'NTOP15EW': 'NIFTY TOP 15 EQUAL WEIGHT',
        'NTOP20EW': 'NIFTY TOP 20 EQUAL WEIGHT',
        'N100Q30': 'NIFTY100 QUALITY 30',
        'NMC150M50': 'NIFTY Midcap150 Momentum 50',
        'N500FCQT30': 'Nifty500 Flexicap Quality 30',
        'N500LV50': 'NIFTY500 LOW VOLATILITY 50',
        'N500M50': 'NIFTY500 MOMENTUM 50',
        'N500Q50': 'NIFTY500 QUALITY 50',
        'N500MQVLV50': 'NIFTY500 MULTIFACTOR MQVLv 50',
        'NMC150Q50': 'NIFTY Midcap150 Quality 50',
        'NSC250Q50': 'Nifty Smallcap250 Quality 50',
        'N500MMCQ50': 'NIFTY500 MULTICAP MOMENTUM QUALITY 50',
        'NMSC400MQ100': 'Nifty MidSmallcap400 Momentum Quality 100',
        'NSC250MQ100': 'Nifty Smallcap250 Momentum Quality 100',
        'NQLV30': 'NIFTY QUALITY LOW VOLATILITY 30',
        'N50EW': 'NIFTY50 EQUAL WEIGHT',
        'N50V20': 'NIFTY50 VALUE 20',
        'N200V30': 'Nifty200 Value 30',
        'N500V50': 'NIFTY500 VALUE 50',
        'N500EW': 'NIFTY500 EQUAL WEIGHT',
        'N200Q30': 'NIFTY200 Quality 30'
    },
    'Thematic': {
        'NBIRLA': 'NIFTY INDIA CORPORATE GROUP INDEX - ADITYA BIRLA GROUP',
        'NCM': 'Nifty Capital Markets',
        'NCOMM': 'NIFTY COMMODITIES',
        'NCHOUS': 'Nifty Core Housing',
        'NCPSE': 'NIFTY CPSE',
        'NENERGY': 'NIFTY ENERGY',
        'NEVNAA': 'Nifty EV & New Age Automotive',
        'NHOUSING': 'Nifty Housing',
        'N100ESG': 'NIFTY100 ESG',
        'N100ESGE': 'NIFTY100 Enhanced ESG',
        'N100ESGSL': 'Nifty100 ESG Sector Leaders',
        'NICON': 'NIFTY INDIA CONSUMPTION',
        'NIDEF': 'Nifty India Defence',
        'NIDIGI': 'Nifty India Digital',
        'NIMFG': 'Nifty India Manufacturing',
        'NNACON': 'NIFTY INDIA NEW AGE CONSUMPTION',
        'NRAIL': 'Nifty India Railways PSU',
        'NTOUR': 'NIFTY INDIA TOURISM',
        'N5CORP': 'NIFTY INDIA SELECT 5 CORPORATE GROUPS (MAATR)',
        'NINFRA': 'NIFTY INFRASTRUCTURE',
        'NMAHIN': 'NIFTY INDIA CORPORATE GROUP INDEX - MAHINDRA GROUP',
        'NIPO': 'NIFTY IPO',
        'NMIDLIQ15': 'NIFTY MIDCAP LIQUID 15',
        'NMSICON': 'Nifty MidSmall India Consumption',
        'NMNC': 'NIFTY MNC',
        'NMOBIL': 'Nifty Mobility',
        'NPSE': 'NIFTY PSE',
        'NREiT': 'Nifty REITs & InvITs',
        'NRURAL': 'Nifty Rural',
        'NNCCON': 'Nifty Non-Cyclical Consumer Index',
        'NSERVSEC': 'NIFTY SERVICES SECTOR',
        'NSH25': 'NIFTY SHARIAH 25',
        'NTATA': 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP',
        'NTATA25': 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP',
        'NTRANS': 'Nifty Transportation & Logistics',
        'NLCLIQ15': 'NIFTY100 LIQUID 15',
        'N50SH': 'NIFTY50 SHARIAH',
        'N500SH': 'NIFTY500 SHARIAH',
        'NMFG532': 'NIFTY500 MULTICAP INDIA MANUFATURING 50:30:20',
        'NINFRA532': 'NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20',
        'NSMEE': 'NIFTY SME EMERGE',
        'NWAVES': 'Nifty Waves'
    }
}

all_indices = [col for col in df.columns if col != 'DATE']

# Calculate 3-year profits for all indices
lookback_days = 756

profits_3yr = {}
for col in all_indices:
    current_price = df[col].iloc[-1]
    price_3yr_ago = df[col].iloc[-lookback_days] if len(df) >= lookback_days else None
    
    if pd.notna(current_price) and pd.notna(price_3yr_ago) and price_3yr_ago > 0:
        profit_percentage = ((current_price - price_3yr_ago) / price_3yr_ago) * 100
        profits_3yr[col] = profit_percentage

# Calculate percentiles
profits_series = pd.Series(profits_3yr)
percentiles = profits_series.rank(pct=True)

# Create categorized results
categorized_results = []

for category_name, indices_dict in categories.items():
    for short_name, full_name in indices_dict.items():
        if full_name in percentiles:
            categorized_results.append({
                'Category': category_name,
                'Short_Name': short_name,
                'Full_Name': full_name,
                'Percentile': percentiles[full_name],
                'Profit_3yr_%': profits_3yr[full_name]
            })

# Create DataFrame and save
results_df = pd.DataFrame(categorized_results)
results_df = results_df.sort_values(['Category', 'Percentile'], ascending=[True, False])

output_file = 'categorized_indices.csv'
results_df.to_csv(output_file, index=False)

print(f"✓ Categorized results saved to: {output_file}")
print(f"\nTotal indices categorized: {len(results_df)}")
print(f"\nBreakdown by category:")
for category in ['Broad', 'Sector', 'Strategy', 'Thematic']:
    count = len(results_df[results_df['Category'] == category])
    print(f"  {category}: {count} indices")

# Display sample from each category
print(f"\n{'='*100}")
print("SAMPLE DATA FROM EACH CATEGORY")
print(f"{'='*100}")

for category in ['Broad', 'Sector', 'Strategy', 'Thematic']:
    category_df = results_df[results_df['Category'] == category]
    print(f"\n{category.upper()} (Top 3):")
    top_3 = category_df.head(3)
    for _, row in top_3.iterrows():
        print(f"  {row['Short_Name']:15} {row['Full_Name']:50} {row['Percentile']:.3f} ({row['Profit_3yr_%']:+6.1f}%)")
