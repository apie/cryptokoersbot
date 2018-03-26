#!/usr/bin/env python3
import sys
import datetime
from db import open_db

def sort_date(elem):
  return elem.get('date')

def get_price_between_dates(coin, min_date, max_date):
  db = open_db()
  price = None
  for rec in sorted((db('abbr')==coin) & (db('date') >= max_date) & (db('date') < min_date),
      key=sort_date):
    price = rec.get('sell')
    break
  return price

def list_changes(coin):
  db = open_db()
  now = datetime.datetime.now()
  historic_moments = [
    {
      '24h': now - datetime.timedelta(hours=24),
    },
    {
      '7d': now - datetime.timedelta(days=7),
    },
    {
      '30d': now - datetime.timedelta(days=30),
    },
    {
      '90d': now - datetime.timedelta(days=90),
    },
  ]
  for rec in sorted((db('abbr')==coin.lower()) & (db('date') > historic_moments[0]['24h']) & (db('date') <= now),
      key=sort_date,
      reverse=True):
    current_price = rec.get('sell')
    break

  line = ''
  previous_moment = now
  for moment in historic_moments:
    min_date = previous_moment
    max_date = list(moment.values())[0]
    price = get_price_between_dates(coin.lower(), min_date, max_date)
    change = ((current_price/price)-1)*100
    line += '%3s' % list(moment.keys())[0]
    line += '%7s' % (' %s%5.2f%%' % ('+' if change >= 0 else '-', abs(change)))
    line += ' %s ' % ('▲' if change >= 0 else '▼') if change is not None else ''
  print(line)

def list_latest(coin):
  db = open_db()
  change = None
  sell_old = None
  for i, r in enumerate(sorted(db._abbr[coin.lower()], key=sort_date, reverse=False)[-11:]):
    sell = r.get('sell')
    change = ((sell/sell_old)-1)*100 if sell_old else None 
    line = ''
    line += r.get('date').strftime('%Y-%m-%d %H:%M')
    line += ' € %9.2f' % r.get('sell')
    line += '%7s' % (' %s%5.2f%%' % ('+' if change >= 0 else '-', abs(change)) if change is not None else '')
    line += ' %s' % ('▲' if change >= 0 else '▼') if change is not None else ''
    if i == 0:
      print('%s (%s)' % (r.get('name'), r.get('abbr').upper()))
    else:
      print(line)
    sell_old = sell

def get_markets():
  db = open_db()
  return " ".join(sorted(db._abbr.keys()))

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print('Geef als argument een of meerdere markten/coins op.')
    print('Beschikbaar: %s' % get_markets())
  else:
    coins = sys.argv[1:]
    for i, coin in enumerate(coins):
      list_latest(coin)
      list_changes(coin)
      print() if i < len(coins)-1 else None

