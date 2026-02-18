import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render(data):
    
    st.markdown("# 🌊 Ripple Effects")
    st.markdown(
        "Tariffs don't stop at the border. "
        "Three chain reactions that affect ordinary people."
    )
    st.markdown("---")
    
    # ── RIPPLE 1: VIETNAM PARADOX ──
    st.markdown("## 🇻🇳 Ripple 1: The Vietnam Paradox")
    st.markdown(
        "*Companies moved factories from China to escape tariffs. "
        "Now Vietnam faces 46% — the highest of any country without a deal.*"
    )
    
    vietnam_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'vietnam_exports': [41, 49, 67, 79, 96, 109, 113, 115],
        'china_exports': [506, 540, 452, 451, 507, 537, 427, 440]
    })
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=vietnam_data['year'],
        y=vietnam_data['vietnam_exports'],
        name='Vietnam → US ($B)',
        mode='lines+markers',
        line=dict(color='#2ca02c', width=3),
        fill='tozeroy',
        fillcolor='rgba(44,160,44,0.1)'
    ))
    
    fig1.add_trace(go.Scatter(
        x=vietnam_data['year'],
        y=vietnam_data['china_exports'],
        name='China → US ($B)',
        mode='lines+markers',
        line=dict(color='#d62728', width=3),
        yaxis='y2'
    ))
    
    fig1.add_annotation(
        x=2019, y=67,
        text="Factories flee<br>China tariffs",
        showarrow=True, arrowcolor='#2ca02c',
        bgcolor='#2ca02c', font=dict(color='white', size=9),
        ax=-70, ay=-50
    )
    
    fig1.add_annotation(
        x=2024, y=115,
        text="Hit with 46%<br>tariff in 2025",
        showarrow=True, arrowcolor='#d62728',
        bgcolor='#d62728', font=dict(color='white', size=9),
        ax=60, ay=-40
    )
    
    fig1.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,29,39,0.8)',
        font=dict(color='#ccd6f6'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(
            title='Vietnam Exports ($B)', 
            color='#2ca02c',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title='China Exports ($B)',
            overlaying='y', side='right',
            color='#d62728'
        ),
        legend=dict(
            bgcolor='rgba(26,29,39,0.8)',
            bordercolor='rgba(255,255,255,0.2)'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("---")
    
    # ── RIPPLE 2: CANADA HOUSING ──
    st.markdown("## 🏠 Ripple 2: Canadian Lumber → US Housing Crisis")
    st.markdown(
        "*A 25% tariff on Canadian lumber doesn't stay at the border. "
        "It travels through the supply chain and ends up in your mortgage.*"
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class='insight-box'>
        <b>The Chain Reaction:</b><br><br>
        🪵 25% tariff on Canadian lumber<br>
        ↓<br>
        📈 US lumber prices rise 6%<br>
        ↓<br>
        🏗️ Home construction cost +$9,000<br>
        ↓<br>
        🏠 Sale price rises $18,000<br>
        ↓<br>
        👨‍👩‍👧 Millions priced out of market<br>
        ↓<br>
        📉 Housing affordability crisis deepens
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        stages = [
            'Canadian Lumber<br>Tariff (25%)',
            'US Lumber<br>Price Increase',
            'Construction<br>Cost Increase',
            'Home Sale<br>Price Increase',
            'Affordability<br>Gap Widens'
        ]
        values = [100, 70, 50, 35, 25]
        colors = ['#d62728', '#ff7f0e', '#ff7f0e', '#ffdd57', '#d62728']
        labels = [
            '+25% tariff rate',
            '+6% per board',
            '+$9,000/house',
            '+$18,000/house',
            '1.3M fewer buyers'
        ]
        
        fig2 = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo='text',
            text=labels,
            marker=dict(color=colors),
            connector=dict(
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            )
        ))
        
        fig2.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ccd6f6'),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # ── RIPPLE 3: INDIA PHARMA ──
    st.markdown("## 💊 Ripple 3: India Pharma — The National Security Risk")
    st.markdown(
        "*India supplies 40% of US generic drugs. "
        "A 26% tariff on Indian goods isn't just economic — "
        "it creates a healthcare supply chain vulnerability.*"
    )
    
    pharma_facts = pd.DataFrame({
        'metric': [
            'India share of\nUS generic drugs',
            'Active ingredients\nsourced from China',
            'US generic drug\nmarket size',
            'Tariff rate on\nIndian goods',
            'Americans using\ngeneric drugs'
        ],
        'value': [40, 70, 300, 26, 60],
        'unit': ['%', '% (India imports from China)',
                 '$B market size', '% (current rate)',
                 '% of population'],
        'color': ['#ff7f0e', '#d62728', '#1f77b4', 
                  '#d62728', '#ff7f0e']
    })
    
    fig3 = go.Figure(go.Bar(
        x=pharma_facts['metric'],
        y=pharma_facts['value'],
        marker_color=pharma_facts['color'],
        text=[f"<b>{v}%</b><br><i>{u}</i>" 
              for v, u in zip(pharma_facts['value'], 
                             pharma_facts['unit'])],
        textposition='outside',
    ))
    
    fig3.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,29,39,0.8)',
        font=dict(color='#ccd6f6'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickangle=-10
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Percentage / Value',
            range=[0, 350]
        ),
        margin=dict(l=10, r=10, t=20, b=10)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info(
        "💡 **Key Insight:** India sources 70% of its pharmaceutical "
        "active ingredients FROM China, then exports finished drugs to the US. "
        "Both the India→US and China→India legs face tariff exposure, "
        "creating a compounding supply chain risk for US healthcare."
    )