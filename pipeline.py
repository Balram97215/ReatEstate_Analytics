"""
Data Loading Pipeline
Handles Google Drive integration and database connectivity
"""
import streamlit as st
import sqlite3
import pandas as pd
import gdown
from pathlib import Path
from config import (
    GOOGLE_DRIVE_FILE_ID,
    DATABASE_PATH,
    DATABASE_FILENAME,
    DB_TIMEOUT,
    DB_CHECK_SAME_THREAD
)


@st.cache_resource
def download_database():
    """
    Download database from Google Drive if not exists
    Uses Streamlit cache to avoid repeated downloads
    """
    if DATABASE_PATH.exists():
        return DATABASE_PATH
    
    try:
        with st.spinner("📥 Downloading database from Google Drive..."):
            url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
            gdown.download(url, str(DATABASE_PATH), quiet=False)
            st.success("✅ Database downloaded successfully!")
        return DATABASE_PATH
    except Exception as e:
        st.error(f"❌ Failed to download database: {e}")
        return None


@st.cache_resource
def get_database_connection():
    """
    Get thread-safe database connection
    CRITICAL: check_same_thread=False for Streamlit compatibility
    """
    db_path = download_database()
    
    if not db_path or not db_path.exists():
        st.error(f"Database not found at {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(
            str(db_path),
            timeout=DB_TIMEOUT,
            check_same_thread=DB_CHECK_SAME_THREAD  # REQUIRED for Streamlit
        )
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"❌ Database connection error: {e}")
        return None


def query_database(sql_query):
    """
    Execute SQL query and return DataFrame
    Handles errors gracefully
    """
    try:
        conn = get_database_connection()
        if conn is None:
            st.error("Database connection unavailable")
            return pd.DataFrame()
        
        df = pd.read_sql(sql_query, conn)
        return df
    
    except pd.errors.DatabaseError as e:
        st.error(f"❌ Query error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return pd.DataFrame()


def get_data_status():
    """Get database connection and data availability status"""
    try:
        conn = get_database_connection()
        if conn is None:
            return {"status": "error", "message": "Cannot connect to database"}
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM silver_parcels")
        count = cursor.fetchone()[0]
        
        return {
            "status": "connected",
            "message": f"✅ Connected | {count:,} properties loaded",
            "record_count": count
        }
    except Exception as e:
        return {"status": "error", "message": f"❌ Error: {str(e)[:50]}"}
