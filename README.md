# Cryptokoersbot

Haal de koersen op via `python3 market_data.py`.

Toon de laatste 10 koersen van een of meerdere munten met `python3 list.py <munt1> <munt2>`.

De koers via `telegram-send` sturen kan als volgt (backticks toevoegen vooraan en achteraan de regel, monospace font afdwingen via markdown):

```python3 list.py <munt1> | sed 's/^/`/' | sed 's/$/`/' | telegram-send --stdin --format markdown```
