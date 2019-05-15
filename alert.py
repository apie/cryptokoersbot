#!/usr/bin/env python3
import sys
from db import open_db

def sort_date(elem):
  return elem.get('date')

def get_change(coin):
  db = open_db()
  vals = []
  for rec in sorted((db('abbr')==coin.lower()),
      key=sort_date,
      reverse=True)[:2]:
    vals.append(rec.get('sell'))
  assert len(vals) == 2
  latest = vals[0]
  previous = vals[1]
  return latest, round(((latest/previous)-1)*100, 2)

if __name__ == '__main__':
  if len(sys.argv) == 2:
    print('Geef als eerste argument een markt/coin op.')
    print('Geef als tweede argument een verschil in procenten. Het script zal de actuele waarde teruggeven als dit percentage is bereikt/overschreden sinds de vorige meting.')
  else:
    coin = sys.argv[1]
    change_check = round(float(sys.argv[2]), 2)
    latest, change = get_change(coin)
    if abs(change) >= change_check:
      print('Munt:', coin.upper())
      print('Koers:', str(latest)[:6])
      print('Verschil:', change)
      sys.exit(1)

