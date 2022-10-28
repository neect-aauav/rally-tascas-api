import json
import requests

import sys
import os
from pathlib import Path
from decouple import config
sys.path.append('../')

BASE_DIR =  Path(os.environ.get('PROD_BASE_DIR')).as_posix() if os.environ.get('PROD_BASE_DIR') else Path(__file__).resolve().parent.parent
BASE_IRI = os.environ.get('BASE_IRI') if os.environ.get('BASE_IRI') else 'http://localhost:8000'

SUPER_USER_TOKEN = os.environ.get('SUPER_USER_TOKEN') if os.environ.get('SUPER_USER_TOKEN') else config('SUPER_USER_TOKEN')

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {SUPER_USER_TOKEN}',
}

TAGS = ['teams', 'games', 'bars', 'prizes']

for tag in TAGS:
    # generate <tag> from <tag>.json
    print(f"Generating {tag}...")
    with open(f'{BASE_DIR}/data/{tag}.json', 'r') as f:
        try:
            objects = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"[Ignored] File {tag}.json is not a valid JSON file or is empty!\n")
            continue

        # generate bar objects
        success = 0
        for object in objects:
            req = requests.post(f'{BASE_IRI}/api/{tag}', json=object, headers=HEADERS)
            response = req.json()
            print(f"  [{response['status']}] {response['message']}")
            if req.status_code == 200:
                success += 1

        print(f"Generated {success}/{len(objects)} {tag}!\n")