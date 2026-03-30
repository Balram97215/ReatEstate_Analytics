# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

### Step 3: Open in Browser
The app will automatically open at `http://localhost:8501`

## 📊 What You Get

### 👥 Institutional Ownership Dashboard
- Total institutional vs individual property count
- Distribution by value and portfolio composition
- Top 15 institutional owners
- County-level ownership analysis
- Market concentration metrics

### ⚠️ Market Risk Dashboard
- Risk score distribution and trends
- High-risk property alerts
- Risk metrics by property use type
- Institutional vs Individual risk exposure
- County and market segment analysis

## 🔄 Data Pipeline

1. **First Run**: App downloads florida_housing.db from Google Drive (120MB)
   - Download happens automatically on first launch
   - Takes ~5-10 seconds
   - Cached for subsequent runs

2. **Subsequent Runs**: Uses cached database
   - Data queries cached for 1 hour
   - Zero download time

3. **Database**: 100,000+ Florida property records
   - Column mapping to queries
   - Real-time filtering and aggregation

## 📁 Project Structure

```
RealEstate_Analytics/
├── app.py                          # Main entry point
├── config.py                       # Configuration & constants
├── pipeline.py                     # Data loading (Google Drive)
├── queries.py                      # Pre-built analytics queries
├── requirements.txt                # Dependencies
├── README.md                       # Documentation
├── DEPLOYMENT.md                   # Deployment guide
├── verify_setup.py                 # Setup verification script
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── .gitignore                     # Git exclusions
├── pages/
│   ├── 01_institutional_ownership.py
│   └── 02_market_risk.py
└── data/                          # Database stored here
    └── florida_housing.db         # (Downloaded on first run)
```

## 🔑 Key Features

✅ **Zero Errors** - All code tested and validated  
✅ **Automatic Download** - Seamless Google Drive integration  
✅ **Smart Caching** - Queries cached for performance  
✅ **Clean Design** - Professional UI with Plotly charts  
✅ **Thread-Safe** - Streamlit compatibility guaranteed  
✅ **Scalable** - Handles 100k+ records efficiently  

## 🎯 Common Tasks

### View Database Info
```bash
python3 verify_setup.py
```

### Clear Cache
```bash
rm -rf .streamlit_cache/
rm -rf data/
```

### Deploy to Streamlit Cloud
See `DEPLOYMENT.md` for Streamlit Cloud instructions

## 🆘 Troubleshooting

**App won't start?**
- Run `python3 verify_setup.py`
- Check Python version is 3.8+
- Ensure all packages installed

**Database doesn't download?**
- Check internet connection
- Verify Google Drive link is accessible
- Check `config.py` for correct file ID

**Queries are slow?**
- First run will download data (normal)
- Subsequent runs use cache
- Clear cache if having issues: `rm -rf .streamlit_cache/`

## 📞 Next Steps

1. Customize queries in `queries.py`
2. Add new pages in `pages/` directory
3. Deploy to Streamlit Cloud (see DEPLOYMENT.md)
4. Share dashboard with stakeholders

---

**Status**: ✅ Ready to Deploy
**Database**: 100,000 properties
**Last Updated**: March 30, 2026
