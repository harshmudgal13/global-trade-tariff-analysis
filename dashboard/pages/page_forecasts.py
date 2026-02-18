import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def render(data):
    
    st.markdown("# 🔮 Trade Flow Forecasts (2025–2027)")
    st.markdown(
        "Forecasts show the projected gap between "
        "**baseline trade growth** and **tariff-adjusted reality**. "
        "The wider the gap, the bigger the tariff's cost."
    )
    st.markdown("---")
    
    forecasts = data.get('forecasts', pd.DataFrame())
    
    if forecasts.empty:
        st.warning(
            "Forecast data not found. "
            "Run notebooks/06_forecasting.ipynb first."
        )
        return
    
    # Controls
    col1, col2 = st.columns([2, 1])
    with col1:
        countries = forecasts['country_name'].unique().tolist()
        selected_countries = st.multiselect(
            "Select countries to compare:",
            options=countries,
            default=countries[:4]
        )
    with col2:
        metric = st.selectbox(
            "Metric:",
            options=['exports', 'imports'],
            index=0
        )
    
    if not selected_countries:
        st.info("Select at least one country above")
        return
    
    filtered = forecasts[
        (forecasts['country_name'].isin(selected_countries)) &
        (forecasts['metric'] == metric)
    ]
    
    if filtered.empty:
        st.warning("No forecast data for selected countries/metric")
        return
    
    # ── FORECAST CHARTS ──
    n = len(selected_countries)
    cols = 2
    rows = (n + 1) // 2
    
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=selected_countries,
        vertical_spacing=0.15,
        horizontal_spacing=0.08
    )
    
    positions = [(r+1, c+1) for r in range(rows) for c in range(cols)]
    
    for idx, country in enumerate(selected_countries):
        if idx >= len(positions):
            break
            
        row, col = positions[idx]
        country_data = filtered[filtered['country_name'] == country]
        historical = country_data[~country_data['is_forecast']]
        future = country_data[country_data['is_forecast']]
        
        # Historical
        if not historical.empty and 'actual' in historical.columns:
            fig.add_trace(go.Scatter(
                x=historical['year'],
                y=historical['actual'],
                name='Historical' if idx == 0 else None,
                showlegend=(idx == 0),
                mode='lines+markers',
                line=dict(color='#00d4ff', width=2),
                marker=dict(size=6)
            ), row=row, col=col)
        
        # Confidence interval
        if not future.empty:
            fig.add_trace(go.Scatter(
                x=list(future['year']) + list(future['year'])[::-1],
                y=list(future['yhat_upper']) + list(future['yhat_lower'])[::-1],
                fill='toself',
                fillcolor='rgba(0,212,255,0.1)',
                line=dict(color='rgba(0,0,0,0)'),
                name='80% Confidence' if idx == 0 else None,
                showlegend=(idx == 0)
            ), row=row, col=col)
            
            # Baseline forecast
            fig.add_trace(go.Scatter(
                x=future['year'],
                y=future['yhat'],
                name='Baseline Forecast' if idx == 0 else None,
                showlegend=(idx == 0),
                mode='lines+markers',
                line=dict(color='#00d4ff', width=2, dash='dash'),
                marker=dict(size=6, symbol='diamond')
            ), row=row, col=col)
            
            # Tariff-adjusted forecast
            if 'yhat_tariff_adjusted' in future.columns:
                fig.add_trace(go.Scatter(
                    x=future['year'],
                    y=future['yhat_tariff_adjusted'],
                    name='Tariff-Adjusted' if idx == 0 else None,
                    showlegend=(idx == 0),
                    mode='lines+markers',
                    line=dict(color='#d62728', width=2, dash='dash'),
                    marker=dict(size=6, symbol='x')
                ), row=row, col=col)
    
    fig.update_layout(
        height=max(500, rows * 280),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,29,39,0.8)',
        font=dict(color='#ccd6f6'),
        title=dict(
            text=(
                f'<b>Trade {metric.title()} Forecasts — '
                f'Baseline vs. Tariff-Adjusted</b><br>'
                f'<sup>Red line = projected impact of current US tariff rates</sup>'
            ),
            font=dict(color='#ccd6f6')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ── INSIGHT BOX ──
    st.markdown("""
    <div class='insight-box'>
    <b>📖 How to Read These Charts:</b><br><br>
    • <b>Blue solid line</b> = actual historical trade values<br>
    • <b>Blue dashed line</b> = where trade would go WITHOUT tariffs<br>
    • <b>Red dashed line</b> = where trade is projected to go WITH current tariffs<br>
    • <b>Shaded area</b> = 80% confidence interval<br><br>
    The <b>gap between blue and red</b> = the economic cost of tariffs on trade flows.
    </div>
    """, unsafe_allow_html=True)