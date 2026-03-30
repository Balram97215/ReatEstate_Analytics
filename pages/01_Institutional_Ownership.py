"""
Page 1: Institutional Ownership Analysis
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from queries import (
    get_ownership_summary,
    get_ownership_distribution,
    get_owner_type_breakdown,
    get_top_corporate_owners,
    get_ownership_by_county,
    get_institutional_concentration
)

st.set_page_config(page_title="Institutional Ownership", page_icon="👥", layout="wide")

st.title("👥 Institutional Ownership Analysis")
st.markdown("Corporate vs individual property ownership distribution and concentration analysis")

# ============================================================================
# SECTION 1: KEY METRICS
# ============================================================================
st.markdown("## Key Metrics")

col1, col2, col3, col4 = st.columns(4)

try:
    summary = get_ownership_summary()
    
    if not summary.empty:
        total = int(summary['total_properties'].values[0])
        corporate = int(summary['corporate_owned'].values[0])
        individual = int(summary['individual_owned'].values[0])
        corp_pct = float(summary['corporate_pct'].values[0])
        
        with col1:
            st.metric("Total Properties", f"{total:,}")
        with col2:
            st.metric("Institutional", f"{corporate:,}", f"{corp_pct:.1f}%")
        with col3:
            st.metric("Individual", f"{individual:,}", f"{100-corp_pct:.1f}%")
        with col4:
            ratio = corporate / individual if individual > 0 else 0
            st.metric("Institutional Ratio", f"1:{1/ratio:.2f}", f"{ratio:.2%}")
    else:
        st.error("Unable to load summary data")
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 2: OWNERSHIP DISTRIBUTION
# ============================================================================
st.markdown("## Ownership Distribution")

col1, col2 = st.columns(2)

try:
    with col1:
        st.subheader("Properties by Type")
        dist_df = get_ownership_distribution()
        
        if not dist_df.empty:
            fig = px.pie(
                dist_df,
                values='count',
                names='ownership_type',
                color_discrete_map={'Institutional': '#FF6B6B', 'Individual': '#4ECDC4'},
                title="Count Distribution"
            )
            fig.update_traces(textposition='auto', textinfo='value+percent')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Portfolio Value Distribution")
        
        if not dist_df.empty:
            fig = px.pie(
                dist_df,
                values='total_value',
                names='ownership_type',
                color_discrete_map={'Institutional': '#FF6B6B', 'Individual': '#4ECDC4'},
                title="Value Distribution"
            )
            fig.update_traces(textposition='auto', textinfo='value')
            st.plotly_chart(fig, use_container_width=True)
            
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 3: OWNER TYPE BREAKDOWN
# ============================================================================
st.markdown("## Owner Type Breakdown")

try:
    owner_types = get_owner_type_breakdown()
    
    if not owner_types.empty and len(owner_types) > 0:
        # Bar chart
        fig = px.bar(
            owner_types,
            x='owner_type',
            y='count',
            color='count',
            color_continuous_scale='Viridis',
            title="Properties by Owner Type",
            labels={'owner_type': 'Owner Type', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### Detailed Breakdown")
        display_df = owner_types.copy()
        display_df['avg_property_value'] = display_df['avg_property_value'].apply(lambda x: f"${x:,.0f}")
        display_df['total_value'] = display_df['total_value'].apply(lambda x: f"${x:,.0f}")
        display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df[['owner_type', 'count', 'percentage', 'avg_property_value']], 
                    use_container_width=True, hide_index=True)
    else:
        st.info("No owner type data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 4: TOP INSTITUTIONAL OWNERS
# ============================================================================
st.markdown("## Top Institutional Owners")

try:
    top_owners = get_top_corporate_owners(limit=15)
    
    if not top_owners.empty and len(top_owners) > 0:
        # Bar chart
        fig = px.bar(
            top_owners.sort_values('portfolio_value', ascending=True),
            y='owner_name',
            x='portfolio_value',
            orientation='h',
            color='properties',
            color_continuous_scale='RdYlGn',
            title="Top 15 Institutional Owners by Portfolio Value"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### Detailed List")
        display_df = top_owners.copy()
        display_df['portfolio_value'] = display_df['portfolio_value'].apply(lambda x: f"${x:,.0f}")
        display_df['avg_value'] = display_df['avg_value'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(display_df[['owner_name', 'owner_type', 'properties', 'portfolio_value', 'avg_risk']],
                    use_container_width=True, hide_index=True)
    else:
        st.info("No institutional owner data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 5: COUNTY ANALYSIS
# ============================================================================
st.markdown("## Ownership by County")

try:
    by_county = get_ownership_by_county()
    
    if not by_county.empty and len(by_county) > 0:
        # Stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=by_county['county'],
            y=by_county['corporate'],
            name='Institutional',
            marker_color='#FF6B6B'
        ))
        
        fig.add_trace(go.Bar(
            x=by_county['county'],
            y=by_county['individual'],
            name='Individual',
            marker_color='#4ECDC4'
        ))
        
        fig.update_layout(
            barmode='stack',
            title="Property Count by County",
            xaxis_title="County",
            yaxis_title="Properties",
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.markdown("### County Details")
        display_df = by_county.copy()
        display_df['corp_pct'] = display_df['corp_pct'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No county data available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# ============================================================================
# SECTION 6: CONCENTRATION ANALYSIS
# ============================================================================
st.markdown("## Market Concentration")

try:
    conc = get_institutional_concentration()
    
    if not conc.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        inst_value_pct = float(conc['institutional_value_pct'].values[0])
        unique_inst = int(conc['unique_institutional'].values[0])
        unique_indiv = int(conc['unique_individual'].values[0])
        total_owners = int(conc['total_unique_owners'].values[0])
        
        with col1:
            st.metric("Inst. Value %", f"{inst_value_pct:.1f}%")
        with col2:
            st.metric("Institutional Entities", unique_inst)
        with col3:
            st.metric("Individual Owners", unique_indiv)
        with col4:
            st.metric("Total Unique Owners", total_owners)
        
        st.info(f"""
        **Market Concentration Insights:**
        - Institutional entities control **{inst_value_pct:.1f}%** of total property value
        - These represent **{unique_inst:,}** unique institutional entities
        - Compared to **{unique_indiv:,}** individual property owners
        - Concentration ratio: **{inst_value_pct / (100-inst_value_pct):.2f}x**
        """)
    else:
        st.info("Concentration data not available")
        
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")
st.markdown("""
    **Last Updated:** Real-time from database  
    **Data Source:** Florida housing records  
    **Methodology:** Ownership type determined from corporate entity indicators
    """)
