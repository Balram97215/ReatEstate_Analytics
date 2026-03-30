"""
Configuration and constants for Real Estate Analytics
"""
import os
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / ".streamlit_cache"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Google Drive Configuration
GOOGLE_DRIVE_FILE_ID = "1-0N4gGZ-I63sVvFqGHWAlWBSghEjYyAu"
DATABASE_FILENAME = "florida_housing.db"
DATABASE_PATH = DATA_DIR / DATABASE_FILENAME

# Database Configuration
DB_TIMEOUT = 30
DB_CHECK_SAME_THREAD = False

# Streamlit Settings
STREAMLIT_CONFIG = {
    "page_title": "Real Estate Analytics",
    "page_icon": "🏢",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Color Scheme
COLORS = {
    "institutional": "#FF6B6B",
    "individual": "#4ECDC4",
    "low_risk": "#2ecc71",
    "medium_risk": "#f39c12",
    "high_risk": "#e74c3c",
    "very_high_risk": "#c0392b"
}

# Risk Categories
RISK_CATEGORIES = {
    "Low": (0.0, 0.25),
    "Medium": (0.25, 0.40),
    "High": (0.40, 0.50),
    "Very High": (0.50, 1.0)
}

# Table Names
TABLES = {
    "silver_parcels": "silver_parcels",
    "dim_owner": "dim_owner",
    "dim_geography": "dim_geography",
    "dim_property_type": "dim_property_type",
    "fact_property_valuation": "fact_property_valuation"
}

# Analytics Settings
TOP_OWNERS_LIMIT = 15
HIGH_RISK_THRESHOLD = 0.45
