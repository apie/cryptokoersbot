#!/usr/bin/env python3
import requests
import datetime
import time
from db import open_db

api_url_markets = 'https://api.litebit.eu/markets'

def fetch_market_data():
  resp = requests.get(api_url_markets, timeout=3)
  if not resp.status_code == 200:
    raise Exception('Could not read API (%s)' % resp.status_code)
  if not 'application/json' in resp.headers.get('Content-Type'):
    raise Exception('Could not read API')
  try:
    resp.json()
  except:
    raise Exception('Could not decode API json')
  if not resp.json().get('success'):
    raise Exception('API returned an error')
  return resp.json()['result']

def save_market_data(result):
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
      
def fetch_and_save_market_data():
    md = None
    for i in enumerate(range(0,3)):
        try:
            md = fetch_market_data()
            break
        except Exception as e:
            pass
        time.sleep(2)

    if md:
        save_market_data(md)
    else:
        print('Unable to get data')

if __name__ == '__main__':
    fetch_and_save_market_data()

