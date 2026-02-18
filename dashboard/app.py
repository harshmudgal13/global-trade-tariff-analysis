"""
Streamlit Application Entry Point

This file initializes the Global Trade & Tariff Impact Analysis dashboard.
It handles page routing, layout styling, sidebar navigation, and data loading.

Author: Harsh Mudgal
Date: February 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Allow dashboard to import custom modules from /src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Page Configuration
st.set_page_config(
    page_title="Global Trade & Tariff Impact Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling

st.markdown("""
<style>
    /* Main background */
    .main { background-color: #0e1117; }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1d27 0%, #16213e 100%);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Metric values */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #00d4ff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Metric labels */
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #8892b0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e1a 0%, #0e1117 100%);
        border-right: 1px solid #2d3561;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ccd6f6 !important;
    }
    
    /* Risk badge styling */
    .risk-critical {
        background: #d62728;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .risk-high {
        background: #ff7f0e;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .risk-medium {
        background: #f9d62e;
        color: black;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .risk-low {
        background: #2ca02c;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* Section dividers */
    .section-header {
        border-left: 4px solid #00d4ff;
        padding-left: 15px;
        margin: 25px 0 15px 0;
    }
    
    /* Info boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a1d27, #16213e);
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading to avoid repeated disk reads and improve performance

@st.cache_data
def load_all_data():
    """
Load all project datasets and cache them for performance.

Returns:
    dict: Dictionary containing trade data, tariff profiles,
          sector exposure, forecasts, and event timelines.
"""

    
    base = os.path.join(os.path.dirname(__file__), '..')
    
    data = {}
    
    # Core trade data
    try:
        data['trade'] = pd.read_csv(f'{base}/data/processed/trade_data_global.csv')
    except:
        data['trade'] = pd.DataFrame()
    
    # Tariff master reference
    try:
        data['tariff_master'] = pd.read_csv(f'{base}/data/reference/trade_war_master.csv')
    except:
        data['tariff_master'] = pd.DataFrame()
    
    # Trade war events timeline
    try:
        data['events'] = pd.read_csv(f'{base}/data/reference/trade_war_events.csv')
    except:
        data['events'] = pd.DataFrame()

    # Sector exposure
    try:
        data['sectors'] = pd.read_csv(f'{base}/data/reference/sector_exposure.csv')
    except:
        data['sectors'] = pd.DataFrame()
    
    # Forecasts
    try:
        data['forecasts'] = pd.read_csv(f'{base}/data/processed/trade_forecasts.csv')
    except:
        data['forecasts'] = pd.DataFrame()
    
    return data

data = load_all_data()

# Sidebar Navigation UI

with st.sidebar:
    st.markdown("## 🌍 Global Trade Analysis")
    st.markdown("*US Tariff War Impact Dashboard*")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        options=[
            "🌐 Global Overview",
            "🔍 Country Deep Dive",
            "🏭 Sector Risk Analysis",
            "🔮 Trade Forecasts",
            "🌊 Ripple Effects"
        ],
        index=0
    )
    
    st.markdown("---")

    st.markdown("**Last Updated:** Feb 2026")
    st.markdown("**Data Sources:**")
    st.markdown("- World Bank API")
    st.markdown("- UN Comtrade")
    st.markdown("- USTR Official Data")
    
    st.markdown("---")
    st.markdown(
        "<small>Built by [Harsh Mudgal] | "
        "[GitHub](https://github.com/harshmudgal13)</small>",
        unsafe_allow_html=True
    )

# Page Router – dynamically loads each dashboard section

if page == "🌐 Global Overview":
    from pages.page_overview import render
    render(data)

elif page == "🔍 Country Deep Dive":
    from pages.page_country import render
    render(data)

elif page == "🏭 Sector Risk Analysis":
    from pages.page_sectors import render
    render(data)

elif page == "🔮 Trade Forecasts":
    from pages.page_forecasts import render
    render(data)

elif page == "🌊 Ripple Effects":
    from pages.page_ripple import render
    render(data)