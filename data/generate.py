import json
import requests

import sys
sys.path.append('../')

from neectrally.secrets import SUPER_USER_TOKEN

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {SUPER_USER_TOKEN}',
}

TAGS = ['teams', 'bars', 'games', 'prizes']

for tag in TAGS:
    # generate <tag> from <tag>.json
    print(f"Generating {tag}...")
    with open(f'{tag}.json', 'r') as f:
        try:
            objects = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"[Ignored] File {tag}.json is not a valid JSON file or is empty!\n")
            continue

        # generate bar objects
        success = 0
        for object in objects:
            req = requests.post(f'http://localhost:8000/api/{tag}', json=object, headers=HEADERS)
            response = req.json()
            print(f"  [{response['status']}] {response['message']}")
            if req.status_code == 200:
                success += 1

        print(f"Generated {success}/{len(objects)} {tag}!\n")