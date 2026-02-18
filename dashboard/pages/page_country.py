import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Country profiles — the stories behind the data
COUNTRY_PROFILES = {
    'China': {
        'flag': '🇨🇳',
        'headline': 'The Trade War Epicenter',
        'story': """China was the primary target of US tariffs, 
        facing a peak rate of 145% — effectively blocking most trade. 
        After the Nov 2025 Xi-Trump meeting, a truce reduced rates to 30%, 
        but uncertainty remains as the deal expires Nov 2026.""",
        'key_sectors': ['Electronics', 'Steel', 'Electric Vehicles'],
        'peak_tariff': 145,
        'current_tariff': 30,
        'deal_status': 'Extended Truce (until Nov 2026)',
        'gdp_impact_est': '-1.2% GDP growth reduction'
    },
    'Viet Nam': {
        'flag': '🇻🇳',
        'headline': 'The Paradox Economy',
        'story': """Vietnam attracted factories fleeing China tariffs 
        from 2018-2024, becoming a top US supplier. Then in 2025, 
        the US hit Vietnam with 46% tariffs — the highest of any 
        country without a deal. Companies are now evaluating moving 
        factories again, creating massive uncertainty.""",
        'key_sectors': ['Electronics', 'Textiles', 'Footwear'],
        'peak_tariff': 46,
        'current_tariff': 46,
        'deal_status': 'No Deal — Most Exposed',
        'gdp_impact_est': '-3.5% GDP growth reduction'
    },
    'India': {
        'flag': '🇮🇳',
        'headline': 'The Diplomatic Win',
        'story': """India faced a unique double-hit: 26% reciprocal 
        tariff plus an additional 25% "secondary tariff" for buying 
        Russian oil. After diplomatic negotiations, the secondary 
        tariff was lifted Feb 6, 2026. An interim deal reduces 
        rates to 18% on some goods — the most recent development 
        in the entire tariff war.""",
        'key_sectors': ['Pharmaceuticals', 'IT Services', 'Textiles'],
        'peak_tariff': 51,
        'current_tariff': 18,
        'deal_status': 'Interim Agreement — Feb 2026',
        'gdp_impact_est': '-0.8% GDP growth reduction'
    },
    'Canada': {
        'flag': '🇨🇦',
        'headline': 'The Surprising Target',
        'story': """Canada — the US's largest trading partner and 
        closest ally — was hit with 25% tariffs from day one. 
        USMCA-compliant goods are partially exempt, but the 
        relationship has been severely strained. The lumber tariff 
        alone is raising US home prices by $9,000-18,000 per house.""",
        'key_sectors': ['Lumber', 'Auto Parts', 'Energy'],
        'peak_tariff': 35,
        'current_tariff': 25,
        'deal_status': 'No Full Deal — USMCA Applies',
        'gdp_impact_est': '-2.1% GDP growth reduction'
    },
    'Mexico': {
        'flag': '🇲🇽',
        'headline': 'The Supply Chain Hub',
        'story': """Mexico is the US's largest auto parts supplier 
        and a critical USMCA manufacturing hub. The 25% tariff 
        threatens decades of integrated supply chains. 
        USMCA-compliant goods have exemptions, but 
        businesses face massive uncertainty about the 
        2026 USMCA review.""",
        'key_sectors': ['Automotive', 'Agriculture', 'Electronics'],
        'peak_tariff': 25,
        'current_tariff': 25,
        'deal_status': 'No Full Deal — USMCA Applies',
        'gdp_impact_est': '-2.8% GDP growth reduction'
    },
    'Germany': {
        'flag': '🇩🇪',
        'headline': 'The EU Negotiation Win',
        'story': """Germany, representing the EU, faced 20% tariffs 
        but the EU negotiated a bloc-wide deal bringing rates to 15%. 
        German automakers (BMW, Mercedes, Volkswagen) were heavily 
        exposed — auto exports to US worth €25B annually. 
        The deal provided relief but uncertainty about future 
        negotiations remains.""",
        'key_sectors': ['Automobiles', 'Machinery', 'Chemicals'],
        'peak_tariff': 20,
        'current_tariff': 15,
        'deal_status': 'Deal Reached — Jul 2025',
        'gdp_impact_est': '-0.5% GDP growth reduction'
    }
}

def render(data):
    
    st.markdown("# 🔍 Country Deep Dive")
    st.markdown(
        "Select any country to explore its complete tariff war story — "
        "from initial exposure to current status."
    )
    st.markdown("---")
    
    trade = data.get('trade', pd.DataFrame())
    tariff_master = data.get('tariff_master', pd.DataFrame())
    sectors = data.get('sectors', pd.DataFrame())
    
    # ── COUNTRY SELECTOR ──
    available_countries = list(COUNTRY_PROFILES.keys())
    selected = st.selectbox(
        "Choose a country:",
        options=available_countries,
        index=0
    )

    profile = COUNTRY_PROFILES[selected]
    
    st.markdown("---")
    
    # ── COUNTRY HEADER ──
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            f"## {profile['flag']} {selected} — {profile['headline']}"
        )
        st.markdown(
            f"<div class='insight-box'>{profile['story']}</div>",
            unsafe_allow_html=True
        )
    
    with col2:
        # Key stats
        st.metric("Peak Tariff Rate", f"{profile['peak_tariff']}%")
        st.metric(
            "Current Tariff Rate",
            f"{profile['current_tariff']}%",
            delta=f"{profile['current_tariff'] - profile['peak_tariff']}% from peak"
        )
        st.info(f"**Status:** {profile['deal_status']}")
        st.warning(f"**Est. GDP Impact:** {profile['gdp_impact_est']}")
    
    st.markdown("---")
    
    # ── TRADE HISTORY CHART ──
    if not trade.empty:
        
        # Try to find matching country data
        possible_names = ['country_name', 'Country', 'country', 
                         'Economy', 'country_code']
        name_col = None
        for col in possible_names:
            if col in trade.columns:
                name_col = col
                break
        
        if name_col:
            country_data = trade[
                trade[name_col].str.contains(
                    selected.split()[0], 
                    case=False, 
                    na=False
                )
            ].copy()
            
            if not country_data.empty and 'year' in country_data.columns:
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📦 Export Trend")
                    
                    if 'exports' in country_data.columns:
                        country_data_sorted = country_data.sort_values('year')

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=country_data_sorted['year'],
                            y=country_data_sorted['exports'],
                            fill='tozeroy',
                            fillcolor='rgba(0,212,255,0.1)',
                            line=dict(color='#00d4ff', width=2),
                            mode='lines+markers',
                            marker=dict(size=6)
                        ))
                        
                        # Mark tariff war period
                        fig.add_vrect(
                            x0=2024.5, x1=2024.9,
                            fillcolor='rgba(214,39,40,0.2)',
                            line_width=0,
                            annotation_text="Tariff War",
                            annotation_position="top"
                        )

                        fig.update_layout(
                            height=280,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(26,29,39,0.8)',
                            font=dict(color='#ccd6f6'),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                            yaxis=dict(
                                gridcolor='rgba(255,255,255,0.1)',
                                title='Export Value (USD)'
                            ),
                            margin=dict(l=10, r=10, t=10, b=10)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### 📥 Import Trend")
                    
                    if 'imports' in country_data.columns:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(
                            x=country_data_sorted['year'],
                            y=country_data_sorted['imports'],
                            fill='tozeroy',
                            fillcolor='rgba(255,127,14,0.1)',
                            line=dict(color='#ff7f0e', width=2),
                            mode='lines+markers',
                            marker=dict(size=6)
                        ))
                        
                        fig2.update_layout(
                            height=280,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(26,29,39,0.8)',
                            font=dict(color='#ccd6f6'),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                            yaxis=dict(
                                gridcolor='rgba(255,255,255,0.1)',
                                title='Import Value (USD)'
                            ),
                            margin=dict(l=10, r=10, t=10, b=10)
                        )
                        st.plotly_chart(fig2, use_container_width=True)
    
    # ── SECTOR EXPOSURE ──
    if not sectors.empty:
        st.markdown("### 🏭 Most Exposed Sectors")
        
        # Map country name to code
        name_to_code = {
            'China': 'CHN', 'Viet Nam': 'VNM', 'India': 'IND',
            'Canada': 'CAN', 'Mexico': 'MEX', 'Germany': 'DEU'
        }
        
        country_code = name_to_code.get(selected)
        
        if country_code and 'country_code' in sectors.columns:
            country_sectors = sectors[
                sectors['country_code'] == country_code
            ].copy()
            
            if not country_sectors.empty:
                for _, row in country_sectors.iterrows():
                    risk = row.get('exposure_level', 'MEDIUM')
                    badge_class = f"risk-{risk.lower()}"
                    
                    col1, col2, col3 = st.columns([2, 1, 3])
                    with col1:
                        st.markdown(f"**{row.get('sector', 'Unknown')}**")
                    with col2:
                        st.markdown(
                            f"<span class='{badge_class}'>{risk}</span>",
                            unsafe_allow_html=True
                        )
                    with col3:
                        st.markdown(
                            f"*{row.get('notes', '')}*",
                        )