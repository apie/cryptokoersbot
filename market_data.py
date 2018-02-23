#!/usr/bin/env python3
import requests
import datetime
from db import open_db

api_url_markets = 'https://api.litebit.eu/markets'

def save_market_data():
  resp = requests.get(api_url_markets, timeout=3)
  if not resp.json()['success']:
    raise Exception('API returned an error')
  result = resp.json()['result']

  db = open_db()
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

