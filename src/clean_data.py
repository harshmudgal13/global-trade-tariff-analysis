import pandas as pd

# Check 1: Trade data
df = pd.read_csv('data/processed/trade_data_global.csv')
print(f"Trade data shape: {df.shape}")
print(f"Countries: {df['country_name'].nunique()}")
print(f"Years: {df['year'].min()} to {df['year'].max()}")
print(f"Columns: {df.columns.tolist()}")

# Check 2: Tariff master
tariff = pd.read_csv('data/reference/trade_war_master.csv')
print(f"\nTariff master shape: {tariff.shape}")
print(f"Countries with tariff data: {len(tariff)}")
print(tariff[['country_name', 'tariff_current_feb2026', 'deal_status']].head())

# Check 3: Forecasts
forecasts = pd.read_csv('data/processed/trade_forecasts.csv')
print(f"\nForecast shape: {forecasts.shape}")
print(f"Countries forecasted: {forecasts['country_name'].nunique()}")
print(f"Years in forecast: {forecasts['year'].min()} to {forecasts['year'].max()}")