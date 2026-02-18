import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render(data):
    
    st.markdown("# 🏭 Sector Risk Analysis")
    st.markdown(
        "Which industries face the greatest exposure "
        "from current US tariff rates?"
    )
    st.markdown("---")
    
    sectors = data.get('sectors', pd.DataFrame())
    tariff_master = data.get('tariff_master', pd.DataFrame())
    
    if sectors.empty:
        st.warning("Sector data not found. Check data/reference/sector_exposure.csv")
        return
    
    # ── TOP METRICS ──
    col1, col2, col3 = st.columns(3)
    
    critical_count = len(sectors[sectors['exposure_level'] == 'CRITICAL'])
    high_count = len(sectors[sectors['exposure_level'] == 'HIGH'])
    total_value = sectors['us_export_value_usd'].sum() / 1e12
    
    with col1:
        st.metric("Critical Risk Sectors", critical_count)
    with col2:
        st.metric("High Risk Sectors", high_count)
    with col3:
        st.metric("Total Trade Value at Risk", f"${total_value:.1f}T")
    
    st.markdown("---")
    
    # ── SECTOR HEATMAP ──
    st.markdown("### 📊 Country-Sector Risk Matrix")
    
    exposure_map = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    sectors['exposure_numeric'] = sectors['exposure_level'].map(exposure_map)
    
    if not tariff_master.empty:
        import country_converter as coco
        cc = coco.CountryConverter()

        tariff_master['country_name'] = cc.convert(names=tariff_master['country_code'].tolist(), to='name_short')

        code_to_name = dict(zip(
            tariff_master['country_code'], 
            tariff_master['country_name']
        ))
    else:
        code_to_name = {}
    
    pivot = sectors.pivot_table(
        index='country_code',
        columns='sector',
        values='exposure_numeric',
        aggfunc='max'
    ).fillna(0)
    
    pivot.index = [code_to_name.get(c, c) for c in pivot.index]
    
    text_map = {0: '', 1: 'LOW', 2: 'MED', 3: 'HIGH', 4: 'CRIT'}
    text_grid = [[text_map.get(int(v), '') for v in row] 
                 for row in pivot.values]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[
            [0, 'rgba(26,29,39,0.5)'],
            [0.25, '#2ca02c'],
            [0.5, '#ffdd57'],
            [0.75, '#ff7f0e'],
            [1.0, '#d62728']
        ],
        text=text_grid,
        texttemplate='%{text}',
        textfont={'size': 10, 'color': 'white'},
        showscale=False,
        hovertemplate=(
            'Country: %{y}<br>'
            'Sector: %{x}<br>'
            'Risk: %{text}<extra></extra>'
        )
    ))
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ccd6f6'),
        xaxis=dict(tickangle=-30, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ── SECTOR RANKING ──
    st.markdown("### 🏆 Most Exposed Sector-Country Pairs")
    
    high_risk = sectors[
        sectors['exposure_level'].isin(['CRITICAL', 'HIGH'])
    ].copy()
    
    if not tariff_master.empty:
        high_risk = high_risk.merge(
            tariff_master[['country_code', 'country_name']],
            on='country_code', how='left'
        )
    
    high_risk['trade_value_bn'] = high_risk['us_export_value_usd'] / 1e9
    high_risk['label'] = (
        high_risk.get('country_name', high_risk['country_code']) + 
        ' — ' + high_risk['sector']
    )
    high_risk = high_risk.sort_values('trade_value_bn', ascending=True)
    
    color_map = {'CRITICAL': '#d62728', 'HIGH': '#ff7f0e'}
    
    fig2 = go.Figure(go.Bar(
        x=high_risk['trade_value_bn'],
        y=high_risk['label'],
        orientation='h',
        marker_color=[
            color_map.get(e, '#ff7f0e') 
            for e in high_risk['exposure_level']
        ],
        text=[
            f"${v:.0f}B" 
            for v in high_risk['trade_value_bn']
        ],
        textposition='outside',
        hovertext=high_risk.get('notes', ''),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Value at Risk: $%{x:.0f}B<br>'
            '%{hovertext}<extra></extra>'
        )
    ))
    
    fig2.update_layout(
        height=max(400, len(high_risk) * 35),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,29,39,0.8)',
        font=dict(color='#ccd6f6'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Annual Trade Value ($B USD)'
        ),
        yaxis=dict(tickfont=dict(size=10)),
        margin=dict(l=10, r=80, t=10, b=10)
    )
    
    st.plotly_chart(fig2, use_container_width=True)