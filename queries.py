"""
Analytics Queries
All data queries for dashboards
"""
from pipeline import query_database
import streamlit as st


# ============================================================================
# INSTITUTIONAL OWNERSHIP QUERIES
# ============================================================================

@st.cache_data(ttl=3600)
def get_ownership_summary():
    """Total institutional vs individual property count"""
    sql = """
    SELECT 
        COUNT(*) as total_properties,
        SUM(CASE WHEN is_corporate = 1 THEN 1 ELSE 0 END) as corporate_owned,
        SUM(CASE WHEN is_corporate = 0 THEN 1 ELSE 0 END) as individual_owned,
        ROUND(SUM(CASE WHEN is_corporate = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as corporate_pct
    FROM silver_parcels
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_ownership_distribution():
    """Distribution with values"""
    sql = """
    SELECT 
        CASE WHEN is_corporate = 1 THEN 'Institutional' ELSE 'Individual' END as ownership_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM silver_parcels), 1) as percentage,
        ROUND(AVG(market_value), 0) as avg_value,
        ROUND(SUM(market_value), 0) as total_value
    FROM silver_parcels
    GROUP BY is_corporate
    ORDER BY is_corporate DESC
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_owner_type_breakdown():
    """Breakdown by owner type"""
    sql = """
    SELECT 
        owner_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM silver_parcels), 1) as percentage,
        ROUND(AVG(market_value), 0) as avg_property_value,
        ROUND(SUM(market_value), 0) as total_value
    FROM silver_parcels
    WHERE owner_type IS NOT NULL AND owner_type NOT IN ('Unknown', '')
    GROUP BY owner_type
    ORDER BY count DESC
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_top_corporate_owners(limit=15):
    """Top corporate owners by property count"""
    sql = f"""
    SELECT 
        own_name as owner_name,
        owner_type,
        COUNT(*) as properties,
        ROUND(SUM(market_value), 0) as portfolio_value,
        ROUND(AVG(market_value), 0) as avg_value,
        ROUND(AVG(vulnerability_score), 2) as avg_risk
    FROM silver_parcels
    WHERE is_corporate = 1 AND own_name IS NOT NULL
    GROUP BY own_name, owner_type
    ORDER BY properties DESC
    LIMIT {limit}
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_ownership_by_county():
    """Institutional vs individual by county"""
    sql = """
    SELECT 
        county_name as county,
        COUNT(*) as total_properties,
        SUM(CASE WHEN is_corporate = 1 THEN 1 ELSE 0 END) as corporate,
        SUM(CASE WHEN is_corporate = 0 THEN 1 ELSE 0 END) as individual,
        ROUND(SUM(CASE WHEN is_corporate = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as corp_pct
    FROM silver_parcels
    WHERE county_name IS NOT NULL AND county_name NOT IN ('Unknown', '')
    GROUP BY county_name
    ORDER BY total_properties DESC
    LIMIT 25
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_institutional_concentration():
    """Market concentration metrics"""
    sql = """
    SELECT 
        ROUND(SUM(CASE WHEN is_corporate = 1 THEN market_value ELSE 0 END) * 100.0 / 
              SUM(market_value), 1) as institutional_value_pct,
        COUNT(DISTINCT CASE WHEN is_corporate = 1 THEN own_name END) as unique_institutional,
        COUNT(DISTINCT CASE WHEN is_corporate = 0 THEN own_name END) as unique_individual,
        COUNT(DISTINCT own_name) as total_unique_owners
    FROM silver_parcels
    WHERE own_name IS NOT NULL
    """
    return query_database(sql)


# ============================================================================
# MARKET RISK QUERIES
# ============================================================================

@st.cache_data(ttl=3600)
def get_risk_summary():
    """Overall risk metrics"""
    sql = """
    SELECT 
        ROUND(AVG(vulnerability_score), 2) as avg_risk,
        ROUND(MIN(vulnerability_score), 2) as min_risk,
        ROUND(MAX(vulnerability_score), 2) as max_risk,
        COUNT(*) as total_properties,
        COUNT(DISTINCT county_name) as counties
    FROM silver_parcels
    WHERE vulnerability_score IS NOT NULL
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_risk_distribution():
    """Properties by risk category"""
    sql = """
    SELECT 
        CASE 
            WHEN vulnerability_score < 30 THEN 'Low'
            WHEN vulnerability_score < 60 THEN 'Medium'
            WHEN vulnerability_score < 80 THEN 'High'
            ELSE 'Very High'
        END as risk_category,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM silver_parcels), 1) as percentage,
        ROUND(AVG(market_value), 0) as avg_value,
        ROUND(AVG(vulnerability_score), 1) as avg_risk_score
    FROM silver_parcels
    WHERE vulnerability_score IS NOT NULL
    GROUP BY risk_category
    ORDER BY 
        CASE 
            WHEN risk_category = 'Low' THEN 1
            WHEN risk_category = 'Medium' THEN 2
            WHEN risk_category = 'High' THEN 3
            WHEN risk_category = 'Very High' THEN 4
        END
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_risk_by_property_use():
    """Risk metrics by property use"""
    sql = """
    SELECT 
        property_use,
        COUNT(*) as properties,
        ROUND(AVG(vulnerability_score), 2) as avg_risk,
        ROUND(MIN(vulnerability_score), 2) as min_risk,
        ROUND(MAX(vulnerability_score), 2) as max_risk,
        ROUND(AVG(market_value), 0) as avg_value
    FROM silver_parcels
    WHERE property_use IS NOT NULL AND property_use NOT IN ('Unknown', '')
    GROUP BY property_use
    ORDER BY avg_risk DESC
    LIMIT 15
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_risk_by_owner_type():
    """Risk exposure by ownership type"""
    sql = """
    SELECT 
        CASE WHEN is_corporate = 1 THEN 'Institutional' ELSE 'Individual' END as owner_type,
        COUNT(*) as properties,
        ROUND(AVG(vulnerability_score), 2) as avg_risk,
        ROUND(SUM(market_value), 0) as total_value,
        ROUND(AVG(act_yr_blt), 0) as avg_property_age
    FROM silver_parcels
    WHERE vulnerability_score IS NOT NULL
    GROUP BY is_corporate
    ORDER BY avg_risk DESC
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_high_risk_properties(threshold=80):
    """High-risk properties alert"""
    sql = f"""
    SELECT 
        own_name as owner_name,
        phy_addr1 as property_address,
        county_name as county,
        property_use,
        market_segment as market_segment,
        vulnerability_score as risk_score,
        market_value as property_value,
        CASE WHEN is_corporate = 1 THEN 'Institutional' ELSE 'Individual' END as owner_type
    FROM silver_parcels
    WHERE vulnerability_score >= {threshold} AND vulnerability_score IS NOT NULL
    ORDER BY vulnerability_score DESC
    LIMIT 100
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_market_segment_risk():
    """Risk analysis by market segment"""
    sql = """
    SELECT 
        mkt_ar as market_segment,
        COUNT(*) as properties,
        ROUND(AVG(vulnerability_score), 2) as avg_risk,
        ROUND(AVG(market_value), 0) as avg_value,
        ROUND(SUM(market_value) * 100.0 / 
              (SELECT SUM(market_value) FROM silver_parcels), 1) as market_share_pct
    FROM silver_parcels
    WHERE mkt_ar IS NOT NULL AND mkt_ar NOT IN ('Unknown', '')
    GROUP BY mkt_ar
    ORDER BY properties DESC
    LIMIT 20
    """
    return query_database(sql)


@st.cache_data(ttl=3600)
def get_risk_by_county():
    """Risk metrics by county"""
    sql = """
    SELECT 
        county_name as county,
        COUNT(*) as properties,
        ROUND(AVG(vulnerability_score), 2) as avg_risk,
        COUNT(CASE WHEN vulnerability_score >= 80 THEN 1 END) as high_risk_count,
        ROUND(COUNT(CASE WHEN vulnerability_score >= 80 THEN 1 END) * 100.0 / COUNT(*), 1) as high_risk_pct
    FROM silver_parcels
    WHERE county_name IS NOT NULL AND vulnerability_score IS NOT NULL
    GROUP BY county_name
    ORDER BY avg_risk DESC
    LIMIT 25
    """
    return query_database(sql)
