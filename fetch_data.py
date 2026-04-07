import requests
import json
import os

API_KEY = os.environ.get('REDASH_API_KEY')
BASE = 'https://redash.rappi.com'

QUERIES = {
    'dr_counter':     130861,
    'dr_picker':      130862,
    'dr_pie':         130863,
    'dr_hora':        130864,
    'dr_detalle':     130869,  # ← era 130870, corregir
    'so_counter':     131326,
    'so_tienda':      131328,
    'so_tipo':        131327,
    'so_detalle':     131330,
    'so_productos':   131329,
    'so_pickers':     131331,
}

def fetch(query_id, warehouse='Todos'):
    res = requests.post(
        f'{BASE}/api/queries/{query_id}/results',
        headers={
            'Authorization': f'Key {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={'parameters': {'warehouse': warehouse}}
    )
    data = res.json()
    return data.get('query_result', {}).get('data', {}).get('rows', [])

print('Fetching data from Redash...')
result = {}
for name, qid in QUERIES.items():
    print(f'  {name}...')
    result[name] = fetch(qid)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, default=str)

print('data.json updated!')
