# Real Estate Analytics Dashboard
# Streamlit deployment with Google Drive data loading
# Institutional Ownership & Market Risk Analysis

## Features
- **Institutional Ownership Dashboard**: Corporate vs individual ownership analysis
- **Market Risk Dashboard**: Risk assessment and vulnerability scoring
- **Data Pipeline**: Automatic data loading from Google Drive
- **Real-time Analytics**: 100k+ property records from Florida

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

## Data Source
- Primary: Google Drive (florida_housing.db)
- Reference: Real-Estate_Pipeline/florida_housing.db

## Architecture
- `app.py` - Main Streamlit entry point
- `pages/` - Multi-page dashboards
- `pipeline/` - Data loading and processing utilities
- `config/` - Configuration and constants
