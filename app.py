"""
Real Estate Analytics Dashboard
Main Streamlit Application
"""
import streamlit as st
from config import STREAMLIT_CONFIG
from pipeline import get_data_status, download_database

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

# Custom styling
st.markdown("""
    <style>
        [data-testid="stMetricValue"] { font-size: 2.5rem; }
        .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
        .st-tabs [role="tab"] { font-size: 1.1rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🏢 Real Estate Analytics Dashboard")
st.markdown("**Institutional Ownership & Market Risk Analysis for Florida Properties**")

# Sidebar
st.sidebar.title("Navigation")
with st.sidebar:
    st.markdown("---")
    
    # Database status
    st.subheader("📊 Data Status")
    status = get_data_status()
    
    if status["status"] == "connected":
        st.success(status["message"])
        st.caption(f"Records: {status.get('record_count', 0):,}")
    else:
        st.error(status["message"])
    
    st.markdown("---")
    
    # Navigation
    st.subheader("📋 Select Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 Institutional", use_container_width=True):
            st.switch_page("pages/01_institutional_ownership.py")
    with col2:
        if st.button("⚠️ Market Risk", use_container_width=True):
            st.switch_page("pages/02_market_risk.py")
    
    st.markdown("---")
    
    # About
    with st.expander("ℹ️ About"):
        st.write("""
        This dashboard provides insights into:
        - **Institutional Ownership**: Corporate vs individual ownership patterns
        - **Market Risk**: Vulnerability assessment and risk distribution
        
        Data loaded from Florida housing records with 100k+ properties.
        """)

# Main content - Welcome
st.markdown("---")

col1, col2, col3 = st.columns(3)

try:
    from queries import get_ownership_summary
    
    summary = get_ownership_summary()
    
    if not summary.empty:
        total = int(summary['total_properties'].values[0])
        corporate = int(summary['corporate_owned'].values[0])
        individual = int(summary['individual_owned'].values[0])
        corp_pct = float(summary['corporate_pct'].values[0])
        
        with col1:
            st.metric("Total Properties", f"{total:,}")
        with col2:
            st.metric("Institutional", f"{corporate:,} ({corp_pct:.1f}%)")
        with col3:
            st.metric("Individual", f"{individual:,} ({100-corp_pct:.1f}%)")
except Exception as e:
    st.error(f"Error loading summary: {e}")

st.markdown("---")

# Quick info
info_col1, info_col2 = st.columns(2)

with info_col1:
    st.info("""
    ### 👥 Institutional Ownership
    Analyze corporate vs individual property ownership patterns across Florida.
    - Top institutional owners
    - County-level concentration
    - Portfolio values and composition
    """)

with info_col2:
    st.warning("""
    ### ⚠️ Market Risk
    Assess property risk and market vulnerability.
    - Risk distribution analysis
    - High-risk property alerts
    - Market segment comparison
    """)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 40px;'>
    <p>Select an analysis from the sidebar to get started</p>
    <p style='font-size: 0.9em;'>Data automatically downloaded from Google Drive on first run</p>
    </div>
    """, unsafe_allow_html=True)
