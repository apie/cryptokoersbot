#!/usr/bin/env python3
import requests
import datetime
import os
from pydblite import Base

api_url_markets = 'https://api.litebit.eu/markets'

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, 'market_data.db')

def save_market_data():
  db = Base(DB_FILE)
  db.create('abbr', 'name', 'available', 'volume', 'buy', 'sell', 'date',
            mode="open")
  if not db.exists():
    raise Exception('Database error')

  resp = requests.get(api_url_markets, timeout=3)
  if not resp.json()['success']:
    raise Exception('API returned an error')

  result = resp.json()['result']
  for coin in result.keys():
      db.insert(
        abbr=result[coin]['abbr'],
        name=result[coin]['name'],
        available=result[coin]['available'],
        volume=result[coin]['volume'],
        buy=result[coin]['buy'],
        sell=result[coin]['sell'],
        date=datetime.datetime.now())
      db.commit()
      
if __name__ == '__main__':
    save_market_data()

