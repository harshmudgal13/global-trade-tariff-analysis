import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
geo_path = BASE_DIR / "data" / "raw" / "countries.geo.json"

with open(geo_path) as f:
    world_geojson = json.load(f)

def render(data):
    
    # ══════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════
    st.markdown("# 🌍 Global Trade & Tariff Impact Analysis")
    st.markdown(
        "### How the US tariff war reshaped global trade in 2025-2026 — "
        "from 2.5% to 27% in 3 months, the highest rate in over a century."
    )
    st.markdown("---")
    
    tariff_master = data.get('tariff_master', pd.DataFrame())
    trade = data.get('trade', pd.DataFrame())
    
    # ══════════════════════════════════════
    # TOP METRICS ROW
    # ══════════════════════════════════════
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Peak US Tariff Rate",
            value="27%",
            delta="▲ from 2.5% baseline",
            delta_color="inverse"
        )
    
    with col2:
        affected_countries = len(tariff_master) - 1 if not tariff_master.empty else 180
        st.metric(
            label="Countries Affected",
            value=f"{affected_countries}+",
            delta="All major economies"
        )
    
    with col3:
        st.metric(
            label="US Household Cost (2026)",
            value="$1,300",
            delta="Per year extra spending",
            delta_color="inverse"
        )
    
    with col4:
        deal_count = len(tariff_master[
            tariff_master['deal_status'].str.contains('Deal', na=False, case=False)
        ]) if not tariff_master.empty and 'deal_status' in tariff_master.columns else 8
        
        st.metric(
            label="Countries with Deals",
            value=str(deal_count),
            delta=f"Out of {affected_countries}+ targeted"
        )
    
    st.markdown("---")
    
    # ══════════════════════════════════════
    # TWO COLUMN LAYOUT
    # ══════════════════════════════════════
    left, right = st.columns([3, 2])
    
    with left:
        st.markdown(
            "<div class='section-header'>"
            "<h3>📈 The Tariff Escalation Timeline (Dec 2024 – Feb 2026)</h3>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Escalation timeline data
        timeline_data = pd.DataFrame({
            'date': ['Dec 2024', 'Feb 2025', 'Mar 2025', 'Apr 2025',
                     'May 2025', 'Aug 2025', 'Nov 2025', 'Feb 2026'],
            'rate': [2.5, 10.5, 13.0, 27.0, 15.0, 18.0, 16.8, 16.8],
            'event': [
                'Pre-tariff baseline',
                'Canada/Mexico/China IEEPA tariffs begin',
                'Steel & Aluminum raised to 25%',
                'Liberation Day — 100-year high',
                'US-China truce partial reduction',
                'Country-specific tariffs resume',
                'Xi-Trump meeting — China truce extended to Nov 2026',
                'India secondary tariff lifted — interim deal'
            ]
        })
        
        fig = go.Figure()
        
        # Danger zone shading
        fig.add_hrect(
            y0=20, y1=30,
            fillcolor="rgba(214,39,40,0.15)",
            line_width=0,
            annotation_text="100-year high territory",
            annotation_position="top right",
            annotation_font_size=9,
            annotation_font_color="#d62728"
        )
        
        # Main escalation line
        fig.add_trace(go.Scatter(
            x=timeline_data['date'],
            y=timeline_data['rate'],
            mode='lines+markers',
            line=dict(color='#d62728', width=3),
            marker=dict(size=10, color='#d62728', line=dict(color='#fff', width=1)),
            hovertext=timeline_data['event'],
            hovertemplate='<b>%{x}</b><br>Rate: %{y}%<br>%{hovertext}<extra></extra>',
            name='Tariff Rate'
        ))
        
        # Liberation Day annotation
        fig.add_annotation(
            x='Apr 2025', y=27,
            text='<b>Liberation Day</b><br>27% — Highest in<br>over 100 years',
            showarrow=True,
            arrowhead=2,
            arrowcolor='#d62728',
            arrowwidth=2,
            bgcolor='#d62728',
            font=dict(color='white', size=9),
            ax=70, ay=-60,
            bordercolor='#fff',
            borderwidth=1
        )
        
        fig.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,29,39,0.9)',
            font=dict(color='#ccd6f6'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.08)',
                tickfont=dict(color='#8892b0', size=10),
                showline=True,
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.08)',
                title=dict(text='Average US Tariff Rate (%)',font=dict(color='#ccd6f6', size=11)),
                tickfont=dict(color='#8892b0'),
                range=[0, 32],
                showline=True,
                linecolor='rgba(255,255,255,0.1)'
            ),
            margin=dict(l=50, r=20, t=20, b=40),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with right:
        st.markdown(
            "<div class='section-header'>"
            "<h3>🎯 Top Vulnerable Countries</h3>"
            "</div>",
            unsafe_allow_html=True
        )
        
        if not tariff_master.empty:
            # Display vulnerability ranking
            display_cols = ['country_name', 'tariff_current_feb2026', 'deal_status']
            available = [c for c in display_cols if c in tariff_master.columns]
            
            if available:
                display_df = tariff_master[
                    tariff_master['country_code'] != 'USA'
                ][available].copy()
                
                if 'tariff_current_feb2026' in display_df.columns:
                    display_df = display_df.sort_values(
                        'tariff_current_feb2026', ascending=False
                    ).head(10)
                    
                    # Rename for display
                    rename_map = {
                        'country_name': 'Country',
                        'tariff_current_feb2026': 'Tariff %',
                        'deal_status': 'Status'
                    }
                    display_df = display_df.rename(columns=rename_map)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=340,
                    hide_index=True
                )
            else:
                st.info("Tariff data columns not found")
        else:
            st.info("Tariff master data not loaded. Check data/reference/trade_war_master.csv")
    
    st.markdown("---")
    
    # ══════════════════════════════════════
    # WORLD MAP VISUALIZATION
    # ══════════════════════════════════════
    st.markdown(
        "<div class='section-header'>"
        "<h3>🗺️ Global Tariff Exposure Map</h3>"
        "</div>",
        unsafe_allow_html=True
    )
    
    if not tariff_master.empty and 'tariff_current_feb2026' in tariff_master.columns:
        map_data = tariff_master[tariff_master['country_code'] != 'USA'].copy()
        
        # Create choropleth map
        fig_map = px.choropleth(
            map_data,
            geojson=world_geojson,
            locations='country_code',
            featureidkey="id",
            color='tariff_current_feb2026',
            hover_name='country_code',
            hover_data={
                'tariff_current_feb2026': ':.1f',
                'deal_status': True,
                'country_code': False
            },
            
            color_continuous_scale=[
                [0, '#2ca02c'],      # Green for low
                [0.2, '#ffdd57'],    # Yellow
                [0.5, '#ff7f0e'],    # Orange
                [1.0, '#d62728']     # Red for critical
            ],
            labels={'tariff_current_feb2026': 'Tariff Rate (%)'},
            range_color=[0, 50]
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        
        fig_map.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ccd6f6'),
            geo=dict(
                bgcolor='rgba(14,17,23,1)',
                lakecolor='rgba(14,17,23,1)',
                landcolor='rgba(26,29,39,1)',
                showland=True,
                showlakes=True,
                showocean=True,
                oceancolor='rgba(14,17,23,1)',
                showcoastlines=True,
                coastlinecolor='rgba(255,255,255,0.15)',
                countrywidth=0,
                projection_type='natural earth'
            ),
            coloraxis_colorbar=dict(
                title=dict(
                    text='Tariff %',
                    font=dict(color='#ccd6f6', size=11)
                ),
                tickfont=dict(color='#8892b0', size=10),
                len=0.7,
                thickness=15,
                bgcolor='rgba(26,29,39,0.8)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=450
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.caption(
            "🟢 Green = low/negotiated rates (0-15%) | 🟡 Yellow = moderate (15-25%) | "
            "🟠 Orange = high (25-35%) | 🔴 Red = critical exposure (35%+). "
            "Grey countries = no specific tariff data available."
        )
    else:
        st.info("Map data not available. Check that tariff_current_feb2026 column exists in trade_war_master.csv")
    
    # ══════════════════════════════════════
    # KEY INSIGHTS CARDS
    # ══════════════════════════════════════
    st.markdown("---")
    st.markdown("### 💡 Key Insights — Three Critical Stories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='insight-box'>
        <h4 style='color: #00d4ff; margin-top: 0;'>🇨🇳 China</h4>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
        Hit with <b>145% tariffs at peak</b> — the highest 
        ever imposed on a major economy in modern history. 
        Reduced to 30% after Nov 2025 Xi-Trump truce, 
        extended to Nov 2026. Uncertainty remains.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='insight-box'>
        <h4 style='color: #00d4ff; margin-top: 0;'>🇻🇳 Vietnam</h4>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
        <b>46% tariff</b> — highest of any country without 
        a deal. Became a manufacturing hub to escape China 
        tariffs 2018-2024, now faces its own crisis. 
        Companies evaluating next moves.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='insight-box'>
        <h4 style='color: #00d4ff; margin-top: 0;'>🇮🇳 India</h4>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
        <b>Most recent development:</b> Feb 6, 2026 — 
        secondary 25% tariff lifted after oil agreement. 
        Interim deal reduces reciprocal rate to 18% on 
        selected goods. Diplomatic win.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ══════════════════════════════════════
    # FOOTER CTA
    # ══════════════════════════════════════
    st.info(
        "👈 **Explore deeper:** Use the sidebar to navigate to "
        "Country Deep Dives, Sector Analysis, Trade Forecasts, and Ripple Effects."
    )