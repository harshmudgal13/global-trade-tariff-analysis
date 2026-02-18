
markdown# Global Trade & Tariff Impact Analysis - Project Plan

## Core Question
How are recent tariff changes (2022-2024) affecting global trade flows and which sectors/countries are most vulnerable?

## Key Metrics I Will Build

1. **Trade Volatility Index**
   - Measure: Month-to-month variance in trade volumes
   - Scale: 0-100 (higher = more volatile)

   - Keyword: Variance.
   - Meaning: Does the line look like a smooth hill or a jagged saw blade? Jagged = High Volatility.

2. **Tariff Exposure Score**
   - Measure: Average tariff rate × trade dependency
   - Shows which countries are most affected

   - Keyword: Dependency.
   - Meaning: If Mexico sends 80% of its cars to the US, and the US adds a 20% tariff, Mexico's "Exposure" is huge.

3. **Trade Flow Forecast**
   - Predict next 6-12 months using historical trends
   - Prophet or simple moving average
   - Keyword: Prophet.
   - Meaning: A library created by Meta (Facebook) that looks at the past 10 years to "guess" where the line will go in 2026.

4. **Sector Risk Rating**
   - Focus on: Automotive, Electronics, Steel
   - Combine tariff data + trade volume data

   - Keyword: Correlation.
   - Meaning: Does a rise in Steel tariffs directly cause a drop in Automotive exports

## Data Sources Confirmed

- [ ] World Bank API: Trade volumes, tariffs, GDP
- [ ] UN Comtrade: Sector-specific data (if needed)
- [ ] Manual: Recent news for 2024-2025 context

## Countries in Focus
1. United States (largest importer)
2. China (manufacturing hub)
3. Germany (EU representative)
4. Mexico (nearshoring beneficiary)
5. India (emerging economy)
6. Vietnam (supply chain diversification)

## Sectors in Focus
1. Automotive (high tariff impact)
2. Electronics (complex supply chains)
3. Steel/Aluminum (direct tariff targets)

## Timeline (this will be changed as per my speed)
- Day 1: ✅ Data exploration and setup
- Day 2: Data cleaning and integration
- Day 3: Metric calculation
- Day 4-5: Forecasting and analysis
- Day 6-7: Dashboard build
- Day 8: Polish and documentation
✅ Action: Customize this based on what data you actually found today.