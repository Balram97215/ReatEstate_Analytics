"""
Page 2: Market Risk Analysis
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from queries import (
    get_risk_summary,
    get_risk_distribution,
    get_risk_by_property_use,
    get_risk_by_owner_type,
    get_high_risk_properties,
    get_market_segment_risk,
    get_risk_by_county
)

st.set_page_config(page_title="Market Risk", page_icon="⚠️", layout="wide")

st.title("⚠️ Market Risk Analysis")
st.markdown("Vulnerability assessment and risk distribution across market segments")

# ============================================================================
# SECTION 1: RISK SUMMARY
# ============================================================================
st.markdown("## Risk Overview")

col1, col2, col3, col4, col5 = st.columns(5)

try:
    risk_summary = get_risk_summary()
    
    if not risk_summary.empty:
        avg_risk = float(risk_summary['avg_risk'].values[0])
        min_risk = float(risk_summary['min_risk'].values[0])
        max_risk = float(risk_summary['max_risk'].values[0])
        total = int(risk_summary['total_properties'].values[0])
        counties = int(risk_summary['counties'].values[0])
        
        with col1:
            st.metric("Avg Risk", f"{avg_risk:.1f}")
        with col2:
            st.metric("Min Risk", f"{min_risk:.1f}")
        with col3:
            st.metric("Max Risk", f"{max_risk:.1f}")
        with col4:
            st.metric("Properties", f"{total:,}")
        with col5:
            st.metric("Counties", counties)
    else:
        st.error("Unable to load risk summary")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 2: RISK DISTRIBUTION
# ============================================================================
st.markdown("## Risk Score Distribution")

col1, col2 = st.columns(2)

try:
    with col1:
        st.subheader("Properties by Category")
        risk_dist = get_risk_distribution()
        
        if not risk_dist.empty and len(risk_dist) > 0:
            color_map = {
                'Low': '#2ecc71',
                'Medium': '#f39c12',
                'High': '#e74c3c',
                'Very High': '#c0392b'
            }
            
            fig = px.bar(
                risk_dist,
                x='risk_category',
                y='count',
                color='risk_category',
                color_discrete_map=color_map,
                title="Properties by Risk Category",
                labels={'risk_category': 'Risk Category', 'count': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Details
            with st.expander("View Details"):
                display_df = risk_dist.copy()
                display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x:.1f}%")
                display_df['avg_value'] = display_df['avg_value'].apply(lambda x: f"${x:,.0f}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No risk distribution data available")
    
    with col2:
        st.subheader("Risk Score Gauge")
        
        if not risk_dist.empty and not risk_summary.empty:
            avg = float(risk_summary['avg_risk'].values[0])
            max_val = float(risk_summary['max_risk'].values[0])
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg,
                title={'text': "Average Risk Score"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "#90EE90"},
                        {'range': [30, 60], 'color': "#FFD700"},
                        {'range': [60, 80], 'color': "#FF8C00"},
                        {'range': [80, 100], 'color': "#FF4500"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_val
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 3: RISK BY PROPERTY USE
# ============================================================================
st.markdown("## Risk by Property Use")

try:
    by_use = get_risk_by_property_use()
    
    if not by_use.empty and len(by_use) > 0:
        fig = px.bar(
            by_use.sort_values('avg_risk', ascending=False),
            x='avg_risk',
            y='property_use',
            orientation='h',
            color='properties',
            color_continuous_scale='YlOrRd',
            title="Average Risk Score by Property Use Type"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### Detailed Analysis")
        display_df = by_use.copy()
        display_df['avg_value'] = display_df['avg_value'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No property use data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 4: RISK BY OWNERSHIP TYPE
# ============================================================================
st.markdown("## Risk Exposure by Ownership Type")

try:
    by_owner = get_risk_by_owner_type()
    
    if not by_owner.empty and len(by_owner) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                by_owner,
                x='owner_type',
                y='avg_risk',
                color='owner_type',
                color_discrete_map={'Institutional': '#FF6B6B', 'Individual': '#4ECDC4'},
                title="Average Risk by Ownership Type",
                labels={'owner_type': 'Owner Type', 'avg_risk': 'Avg Risk'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Metrics
            if len(by_owner) >= 2:
                st.metric("Institutional Avg Risk", 
                         f"{by_owner[by_owner['owner_type'] == 'Institutional']['avg_risk'].values[0]:.2f}")
                st.metric("Individual Avg Risk",
                         f"{by_owner[by_owner['owner_type'] == 'Individual']['avg_risk'].values[0]:.2f}")
                
                diff = abs(by_owner[by_owner['owner_type'] == 'Individual']['avg_risk'].values[0] - 
                          by_owner[by_owner['owner_type'] == 'Institutional']['avg_risk'].values[0])
                st.info(f"**Risk difference:** {diff:.2f} points")
        
        # Table
        st.markdown("### Detailed Comparison")
        display_df = by_owner.copy()
        display_df['total_value'] = display_df['total_value'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No ownership risk data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 5: HIGH-RISK PROPERTIES
# ============================================================================
st.markdown("## High-Risk Properties Alert")

risk_threshold = st.slider("Risk Threshold", min_value=0, max_value=100, value=80, step=5)

try:
    high_risk = get_high_risk_properties(threshold=risk_threshold)
    
    if not high_risk.empty and len(high_risk) > 0:
        st.warning(f"⚠️ Found {len(high_risk)} properties with risk score ≥ {risk_threshold}")
        
        # Display top high-risk properties
        display_df = high_risk.head(20).copy()
        display_df['property_value'] = display_df['property_value'].apply(lambda x: f"${x:,.0f}")
        display_df['risk_score'] = display_df['risk_score'].apply(lambda x: f"{x:.0f}")
        
        st.dataframe(
            display_df[['owner_name', 'property_address', 'county', 'risk_score', 'property_value', 'owner_type']],
            use_container_width=True,
            hide_index=True
        )
        
        if len(high_risk) > 20:
            st.caption(f"Showing 20 of {len(high_risk)} high-risk properties")
    else:
        st.success(f"✅ No properties with risk score ≥ {risk_threshold}")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 6: MARKET SEGMENT ANALYSIS
# ============================================================================
st.markdown("## Market Segment Risk Analysis")

try:
    by_segment = get_market_segment_risk()
    
    if not by_segment.empty and len(by_segment) > 0:
        fig = px.scatter(
            by_segment,
            x='properties',
            y='avg_risk',
            size='avg_value',
            color='market_share_pct',
            hover_name='market_segment',
            color_continuous_scale='Viridis',
            title="Market Segment: Size vs Risk vs Value",
            labels={
                'properties': 'Number of Properties',
                'avg_risk': 'Average Risk',
                'market_share_pct': 'Market Share %'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### Detailed Segment Analysis")
        display_df = by_segment.copy()
        display_df['avg_value'] = display_df['avg_value'].apply(lambda x: f"${x:,.0f}")
        display_df['market_share_pct'] = display_df['market_share_pct'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No market segment data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 7: COUNTY RISK ANALYSIS
# ============================================================================
st.markdown("## Risk Analysis by County")

try:
    by_county = get_risk_by_county()
    
    if not by_county.empty and len(by_county) > 0:
        fig = px.bar(
            by_county.sort_values('avg_risk', ascending=False).head(15),
            x='avg_risk',
            y='county',
            orientation='h',
            color='high_risk_count',
            color_continuous_scale='Reds',
            title="Top 15 Counties by Average Risk",
            labels={'county': 'County', 'avg_risk': 'Avg Risk', 'high_risk_count': 'High Risk Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### County Risk Details")
        display_df = by_county.copy()
        display_df['high_risk_pct'] = display_df['high_risk_pct'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No county risk data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")
st.markdown("""
    **Last Updated:** Real-time from database  
    **Data Source:** Florida housing records  
    **Risk Scoring:** Based on property characteristics and market conditions
    """)
