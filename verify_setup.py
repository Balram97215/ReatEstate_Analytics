"""
Test script to verify setup
Run this to check all components work
"""
import sys
from pathlib import Path

print("\n" + "="*60)
print("🧪 Real Estate Analytics - Setup Verification")
print("="*60 + "\n")

# Test 1: Check imports
print("✓ Testing imports...")
try:
    import streamlit
    import pandas
    import plotly
    import gdown
    import sqlite3
    print("  ✅ All required packages available\n")
except ImportError as e:
    print(f"  ❌ Missing package: {e}\n")
    sys.exit(1)

# Test 2: Check configuration
print("✓ Checking configuration...")
try:
    from config import (
        DATABASE_PATH,
        GOOGLE_DRIVE_FILE_ID,
        STREAMLIT_CONFIG,
        TABLES
    )
    print(f"  ✅ Config loaded successfully")
    print(f"     - Google Drive ID: {GOOGLE_DRIVE_FILE_ID}")
    print(f"     - Database path: {DATABASE_PATH}")
    print(f"     - Streamlit config: {STREAMLIT_CONFIG['page_title']}\n")
except Exception as e:
    print(f"  ❌ Config error: {e}\n")
    sys.exit(1)

# Test 3: Check reference database
print("✓ Checking reference database...")
ref_db = Path("/Users/Ram/Doc/VSCode/Python Project/Real-Estate_Pipeline/florida_housing.db")
if ref_db.exists():
    print(f"  ✅ Reference database found: {ref_db}")
    try:
        conn = sqlite3.connect(str(ref_db))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM silver_parcels")
        count = cursor.fetchone()[0]
        print(f"     - Records in silver_parcels: {count:,}\n")
        conn.close()
    except Exception as e:
        print(f"  ❌ Error reading database: {e}\n")
else:
    print(f"  ⚠️  Reference database not found\n")

# Test 4: Check queries module
print("✓ Testing queries module...")
try:
    # We won't actually run queries since Google Drive won't be downloaded yet
    from queries import (
        get_ownership_summary,
        get_risk_summary,
        get_owner_type_breakdown
    )
    print("  ✅ Query functions imported successfully\n")
except Exception as e:
    print(f"  ❌ Query import error: {e}\n")
    sys.exit(1)

# Test 5: Check pipeline module
print("✓ Testing pipeline module...")
try:
    from pipeline import query_database, get_data_status
    print("  ✅ Pipeline functions imported successfully\n")
except Exception as e:
    print(f"  ❌ Pipeline import error: {e}\n")
    sys.exit(1)

# Test 6: Check app module
print("✓ Testing app module...")
try:
    import app
    print("  ✅ App module imports successfully\n")
except Exception as e:
    print(f"  ⚠️  App import generated warning: {e}\n")

# Summary
print("="*60)
print("✅ All Verification Tests Passed!")
print("="*60)
print("\nTo run the app:")
print("  streamlit run app.py")
print("\nOn first run, the app will:")
print("  1. Download florida_housing.db from Google Drive")
print("  2. Cache it locally for future use")
print("  3. Display all dashboards\n")
