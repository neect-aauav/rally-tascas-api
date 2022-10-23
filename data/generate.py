import json
import requests

import sys
sys.path.append('../')

from neectrally.secrets import SUPER_USER_TOKEN

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {SUPER_USER_TOKEN}',
}

# generate bars from bars.json
print("Generating bars...")

# get bars from json
with open('bars.json', 'r') as f:
    bars = json.load(f)

    # generate bar objects
    success = 0
    for bar in bars:
        req = requests.post('http://127.0.0.1:8000/api/bars', json=bar, headers=HEADERS)
        response =req.json()
        print(response)
        if req.status_code == 200:
            success += 1

    print(f"Generated {success}/{len(bars)} bars!")