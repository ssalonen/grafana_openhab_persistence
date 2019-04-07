from flask import Flask
from flask import request
from flask_cors import CORS
import json
import time
import math
from cryptography.fernet import Fernet

from datetime import datetime
import requests

app = Flask("app")
CORS(app)

with open('key.key', 'rb') as f:
    key = f.read()
    if not key:
        raise ValueError('empty key.key')

with open('secret', 'rb') as f:
    fernet = Fernet(key)
    user_pass = tuple(map(fernet.decrypt, f.readlines()))

def get_items():
    items = requests.get('https://myopenhab.org/rest/items/', auth=user_pass).json()
    items = [entry['name'] for entry in items if entry['type'] != 'Group']
    return items

def to_number(state):
    try:
        return float(state)
    except ValueError:
        return {'CLOSED': 0, 'OPEN': 1}[state]
    
@app.route("/")
def index():
    print(request.__dict__)
    print(request.json)
    return "OK"

@app.route("/search", methods=["POST"])
def grafana_search():
    print(request.json)
    return json.dumps(get_items())

@app.route("/query", methods=["POST"])
def grafana_query():
    print(request.json)
    start, end = request.json['range']['from'], request.json['range']['to']
    targets = [entry['target'] for entry in request.json['targets']]
    
    # only supporting "timeserie"
    out = []
    for target in targets:
        url = f'https://myopenhab.org/rest/persistence/items/{target}?starttime={start}&endtime={end}'
        print(url)
        data = requests.get(url, auth=user_pass).json()
        entry = {}
        entry['target'] = target
        entry['datapoints'] = [[to_number(entry['state']), entry['time']] for entry in data['data']]
        print(f'{target}: {len(entry["datapoints"])}')
        out.append(entry)
    return json.dumps(out)

app.run(debug=False)