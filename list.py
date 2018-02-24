#!/usr/bin/env python3
import sys
from db import open_db

def sort_date(elem):
  return elem.get('date')

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
    line += '%7s' % (' %s%0.2f%%' % ('+' if change >= 0 else '', change) if change is not None else '')
    line += ' %s' % ('▲' if change >= 0 else '▼') if change is not None else ''
    if i == 0:
      print('%s (%s)' % (r.get('name'), r.get('abbr').upper()))
    else:
      print(line)
    sell_old = sell

if __name__ == '__main__':
  coins = sys.argv[1:]
  for i, coin in enumerate(coins):
    list_latest(coin)
    print() if i < len(coins)-1 else None
