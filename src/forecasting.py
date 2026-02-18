"""
Forecasting Module

Uses Facebook Prophet to generate baseline trade forecasts
and applies tariff-based adjustments to simulate policy impact.

Author: Harsh Mudgal
Date: February 2026
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

class TradeForecaster:
    """
    Handles time-series forecasting and tariff-adjusted projections
    for global trade data.
    """
    def __init__(self, trade_data: pd.DataFrame):
        self.data = trade_data
        self.models = {}
        self.forecasts = {}

    def prepare_country_data(self, country_name: str,metric: str = 'exports') -> pd.DataFrame:
        """
        Prepare country-specific data in Prophet-compatible format.
        Converts yearly trade values into ds/y structure.
        """

        country_data = self.data[self.data['country_name'] == country_name].copy()
        country_data = country_data.sort_values('year')
        country_data = country_data.dropna(subset=[metric])
        
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(country_data['year'].astype(str) + '-01-01'),
            'y': country_data[metric].astype(float)
        })
        
        return prophet_df
    
    def forecast_country(self, country_name: str, metric: str = 'exports', periods: int = 3) -> pd.DataFrame:
        """
        Generate baseline forecast for a single country using Prophet.
        Returns historical values plus future projections.
        """

        df = self.prepare_country_data(country_name, metric)

        if len(df) < 4:
            print(f"Not enough data for {country_name}")
            return pd.DataFrame()
        
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.3, 
            interval_width=0.80           
        )
        model.fit(df)

        future = model.make_future_dataframe(periods=periods, freq='YE')
        forecast = model.predict(future)

        self.models[f"{country_name}_{metric}"] = model
        self.forecasts[f"{country_name}_{metric}"] = forecast
        
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        result['year'] = result['ds'].dt.year
        result['country_name'] = country_name
        result['metric'] = metric
        result['is_forecast'] = result['year'] > df['ds'].dt.year.max()
        
        actuals = df.copy()
        actuals['year'] = actuals['ds'].dt.year
        actuals = actuals.rename(columns={'y': 'actual'})
        
        result = result.merge(
            actuals[['year', 'actual']], 
            on='year', 
            how='left'
        )
        return result
    
    def forecast_all_countries(self,
                               countries: list,
                               metric: str = 'exports',
                               periods: int = 3) -> pd.DataFrame:
        """
        Run forecasts for multiple countries and combine outputs
        into a single DataFrame.
        """

        all_forecasts = []
        for country in countries:
            print(f"Forecasting {country}...")
            forecast = self.forecast_country(country, metric, periods)
            if not forecast.empty:
                all_forecasts.append(forecast)
        
        if not all_forecasts:
            return pd.DataFrame()
                
        return pd.concat(all_forecasts, ignore_index=True)
    
    def calculate_tariff_impact_on_forecast(self, forecast_df: pd.DataFrame, tariff_data: pd.DataFrame)-> pd.DataFrame:

        """
        Adjust forecasts to account for tariff war impact.
        
        Logic: Countries with higher tariff exposure will see
        their trade forecasts reduced proportionally.
        
        This is the KEY insight — showing how tariffs bend the forecast curve.
        """
        
        df = forecast_df.copy()
        

        df = df.merge(
            tariff_data[['country_code', 
                         'tariff_current_feb2026', 'tariff_peak']],
            left_on='country_name',
            right_on='country_code',
            how='left'
        )

        # Calculate tariff drag on future forecasts only
        # Higher tariff = bigger reduction in forecast
        # Assumption: Every 10% tariff reduces trade growth by ~3%
        # (Based on economic research on tariff elasticity)

        tariff_drag_factor = (df['tariff_current_feb2026'].fillna(10)) / 10 * 0.03

        df['yhat_tariff_adjusted'] = np.where(
            df['is_forecast'],
            df['yhat'] * (1 - tariff_drag_factor),
            df['yhat']
        )

        df['tariff_drag_amount'] = df['yhat'] - df['yhat_tariff_adjusted']
        
        return df
    
if __name__ == "__main__":
    df = pd.read_csv('data/processed/trade_data_global.csv')
    tariff_master = pd.read_csv('data/reference/trade_war_master.csv')

    df.columns = df.columns.str.strip().str.lower()
    tariff_master.columns = tariff_master.columns.str.strip().str.lower()

    forecaster = TradeForecaster(df)

    # Test on China first
    # Forecast China's Exports
    china_forecast = forecaster.forecast_country('China', 'exports', periods=3)
    
    # the Policy "Drag"
    china_impacted = forecaster.calculate_tariff_impact_on_forecast(china_forecast, tariff_master)
    
    #Compare the "Normal" Future vs "Tariff" Future
    print("CHINA TRADE WAR IMPACT ANALYSIS (2025-2028):")
    print(china_impacted[['year', 'yhat', 'yhat_tariff_adjusted', 'is_forecast']].tail(5))