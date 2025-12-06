# Indian Stock Indices Dashboard

Interactive web dashboard for analyzing 116 Indian stock market indices with percentile rankings, correlation analysis, and portfolio basket management.

## Features

- **Multi-Year Percentile Rankings**: 3-year, 4-year, and 5-year profit percentiles for all 116 indices
- **Interactive Selection**: Click to add indices to your basket for comparison
- **Real-time Metrics**: 
  - 1-year returns
  - Distance from 52-week high/low
  - Percentile rankings (color-coded: green=bottom 20%, red=top 20%)
- **Correlation Matrix**: Pearson correlation analysis between selected indices
- **Four Categories**: Broad Market, Sectoral, Strategy, and Thematic indices

## Data Source

- **Dataset**: 126 Indian stock indices
- **Time Period**: 2005-08-30 to 2025-11-10 (7,378 trading days)
- **Source File**: `data/Latest_Indices_rawdata_14112025.csv`

## Project Structure

```
Right Sector/
├── dashboard.html                          # Main web application (single-file)
├── data/
│   └── Latest_Indices_rawdata_14112025.csv # Source data (126 indices)
├── categorized_indices_updated.csv         # Processed data with 3/4/5-year percentiles
├── basket_data.json                        # Calculated metrics for basket view
├── correlation_matrix.json                 # Pearson correlation matrix (116x116)
├── calculate_4yr_5yr_percentiles.py        # Calculate 4-year and 5-year percentiles
├── calculate_basket_data.py                # Generate basket metrics
├── calculate_correlations.py               # Calculate correlation matrix
├── merge_percentiles.py                    # Merge 3/4/5-year data
└── categorize_indices.py                   # Initial categorization script
```

## Installation & Setup

### Requirements
- Python 3.11+
- pandas 2.3+
- numpy 2.3+

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd "Right Sector"
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate    # Linux/Mac
```

3. **Install dependencies**
```bash
pip install pandas numpy
```

4. **Generate data files** (if needed)
```bash
python calculate_4yr_5yr_percentiles.py
python merge_percentiles.py
python calculate_basket_data.py
python calculate_correlations.py
```

5. **Start local server**
```bash
python -m http.server 8000
```

6. **Open dashboard**
Navigate to `http://localhost:8000/dashboard.html`

## Deployment

### VPS Deployment (Hostinger)

1. **Upload files to VPS** (via SSH/FTP)
```bash
# Create isolated project directory
mkdir -p /var/www/stock-dashboard
cd /var/www/stock-dashboard
```

2. **Required files for deployment**:
   - `dashboard.html`
   - `categorized_indices_updated.csv`
   - `basket_data.json`
   - `correlation_matrix.json`
   - `data/Latest_Indices_rawdata_14112025.csv` (if regenerating data)

3. **Configure web server** (Nginx example):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/stock-dashboard;
    index dashboard.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~ \.(csv|json)$ {
        add_header Cache-Control "no-cache, must-revalidate";
    }
}
```

4. **For Apache** (`.htaccess`):
```apache
DirectoryIndex dashboard.html

<FilesMatch "\.(csv|json)$">
    Header set Cache-Control "no-cache, must-revalidate"
</FilesMatch>
```

## Calculation Methodology

### Percentile Rankings
- **3-Year**: 756 trading days lookback
- **4-Year**: 1,008 trading days lookback
- **5-Year**: 1,260 trading days lookback
- **Formula**: `(rank - 1) / (total_count - 1)` where rank is based on profit percentage
- **Scale**: 0.0 (worst performer) to 1.0 (best performer)

### Color Coding
- **Green (0.0-0.2)**: Bottom 20% performers
- **Yellow-Orange (0.2-0.8)**: Middle performers
- **Red (0.8-1.0)**: Top 20% performers

### Correlation Analysis
- **Method**: Pearson correlation on daily returns
- **Period**: Last 252 trading days (1 year)
- **Range**: 0.0 (no correlation) to 1.0 (perfect correlation)

## Usage

1. **Browse Indices**: Click category tabs (Broad/Sector/Strategy/Thematic)
2. **Sort**: Click "Values ↕" to sort by 5-year percentile
3. **View Details**: Hover over any index to see 3/4/5-year profits and percentiles
4. **Add to Basket**: Click any row to add to comparison basket
5. **Compare**: View side-by-side metrics in basket table
6. **Analyze Correlation**: Select 2+ indices to see correlation matrix
7. **Remove**: Click "Del" to remove from basket

## Data Updates

To update with new market data:

1. Replace `data/Latest_Indices_rawdata_14112025.csv` with new data
2. Run calculation scripts in order:
```bash
python calculate_4yr_5yr_percentiles.py
python merge_percentiles.py
python calculate_basket_data.py
python calculate_correlations.py
```
3. Refresh dashboard

## Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Backend**: Python scripts for data processing
- **Data Format**: CSV and JSON
- **Browser Support**: Modern browsers (Chrome, Firefox, Edge, Safari)
- **Mobile**: Responsive design

## Performance

- **Load Time**: < 2 seconds (all data files ~500KB total)
- **Indices Tracked**: 116 indices across 4 categories
- **Data Points**: 7,378 days × 126 indices = 929,628 data points

## License

[Add your license here]

## Author

[Add your name/contact here]

## Last Updated

December 6, 2025
