import requests
import pandas as pd
import os
from load_dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

COINS = ["btc-bitcoin", "eth-ethereum", "xrp-xrp", "sol-solana"]

for coin_id in COINS:

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}?quotes=USD"

    response = requests.get(url)

    if response.status_code == 200:
         data = response.json()
         df = pd.json_normalize(data)
        #  df= df.drop(columns=['rank',  'total_supply', 'max_supply', 'beta_value', 'first_data_at', 'last_updated', 'quotes.USD.percent_change_15m', 'quotes.USD.percent_change_30m', 'quotes.USD.percent_change_1h', 'quotes.USD.percent_change_6h', 'quotes.USD.percent_change_12h', 'quotes.USD.percent_change_24h', 'quotes.USD.percent_change_7d', 'quotes.USD.percent_change_30d', 'quotes.USD.percent_change_1y', 'quotes.USD.ath_price','quotes.USD.market_cap_change_24h','quotes.USD.percent_from_price_ath','quotes.USD.ath_date'])
   
         df = df[['id', 'name', 'symbol', 'quotes.USD.price', 'quotes.USD.volume_24h','quotes.USD.volume_24h_change_24h', 'quotes.USD.market_cap']]

         df = df.rename(columns={'id': 'coin_id', 'name': 'coin_name', 'symbol': 'coin_symbol', 'quotes.USD.price': 'price_usd', 'quotes.USD.volume_24h': 'volume_24h_usd','quotes.USD.volume_24h_change_24h':'volume_24h_change', 'quotes.USD.market_cap': 'market_cap_usd'})

         DB_USER = os.getenv('DB_USER')
         DB_PASSWORD = os.getenv('DB_PASSWORD')
         DB_HOST = os.getenv('DB_HOST')
         DB_PORT = os.getenv('DB_PORT')
         DB_NAME = os.getenv('DB_NAME')
    
         engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


         df.to_sql('crypto_market_data', con=engine, if_exists='append', index=False)
        
         print(df.head())
    else:        
        print(f"Failed to retrieve data for {coin_id}. Status code: {response.status_code}")

