import requests
import pandas as pd
from typing import List, Optional
import time

class WorldBankAPI:
    """Fetch data from World Bank API"""
    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self):
        self.session = requests.Session()
        self.indicators = {
            'NE.EXP.GNFS.CD': 'exports',
            'NE.IMP.GNFS.CD': 'imports',
            'TM.TAX.MRCH.WM.AR.ZS': 'baseline_tariff',
            'NY.GDP.MKTP.CD': 'gdp',
            'FP.CPI.TOTL.ZG': 'inflation',      # New: Consumer Price Index
            'NY.GDP.PCAP.CD': 'gdp_per_capita'  # New: Wealth per person
        }

    def get_indicator(self, 
                      countries: List[str], 
                      indicator: str, 
                      start_year: int = 2015, 
                      end_year: int = 2024) -> pd.DataFrame:
        
        # Join countries with semicolons: ['USA', 'CHN'] -> "USA;CHN"
        country_str = ';'.join(countries)
        
        # Build the URL address
        url = f"{self.BASE_URL}/country/{country_str}/indicator/{indicator}"

        # 1. Set the instructions for the World Bank
        params = {
            'date': f'{start_year}:{end_year}',
            'format': 'json',
            'per_page': 10000  # Ensures we get all data in one go
        }
                
        # 2. Make the actual request
        print(f"Fetching {indicator} for {len(countries)} countries...")
        response = self.session.get(url, params=params)
                
        # 3. Validation: Did the request fail?
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return pd.DataFrame()
        
        data = response.json()
                
        # 4. Check if we actually got data back
        if len(data) < 2 or not data[1]:
            print("No data returned")
            return pd.DataFrame()
                
        # 5. The "Transformer": Convert JSON into simple rows
        records = []
        for item in data[1]:
            records.append({
                'country_name': item['country']['value'],
                'country_code': item['countryiso3code'],
                'year': int(item['date']),
                'value': item['value'],
                'indicator_code': indicator,
                'indicator_name': item['indicator']['value']
            })
                
        # 6. Turn the rows into a clean DataFrame
        df = pd.DataFrame(records)
        print(f"Retrieved {len(df)} records")
                
        return df
    
    def get_multiple_indicators(self, 
                               countries: List[str], 
                               indicators: List[str], 
                               start_year: int = 2015, 
                               end_year: int = 2024) -> pd.DataFrame:
        """Fetch multiple indicators and combine into single DataFrame"""
        
        all_data = []
        
        for indicator in indicators:
            # Call our worker function for each indicator
            df = self.get_indicator(countries, indicator, start_year, end_year)
            all_data.append(df)
            
            # The "Be Polite" Pause: Wait 0.5 seconds between calls
            time.sleep(0.5) 
                
        # Combine all separate tables into one giant one
        combined = pd.concat(all_data, ignore_index=True)
                
        return combined
    
    # This part only runs if you run this file directly
if __name__ == "__main__":
    # 1. Initialize our machine
    wb = WorldBankAPI()
    
    # 2. Define our target countries (from your Project Plan)
    target_countries = ['USA', 'CHN', 'DEU', 'MEX', 'IND', 'VNM']
    
    # 3. Define the indicators (Export value in USD)
    # NE.EXP.GNFS.CD is the World Bank code for 'Exports of goods and services'
    indicator_code = 'NE.EXP.GNFS.CD'
    
    # 4. Run the fetcher
    test_df = wb.get_indicator(target_countries, indicator_code)
    
    # 5. Show the result
    print("\n--- TEST SUCCESSFUL ---")
    print(test_df.head())