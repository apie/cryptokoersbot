#!/usr/bin/env python3
import os
from pydblite import Base

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, 'market_data.db')

def open_db():
  db = Base(DB_FILE)
  db.create('abbr', 'name', 'available', 'volume', 'buy', 'sell', 'date',
            mode="open")
  if not db.exists():
    raise Exception('Database error')
  db.create_index('abbr')
  return db

