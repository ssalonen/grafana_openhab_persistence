import json
import time
import math
from datetime import datetime

import numpy as np
import pandas as pd
import requests

from flask import Flask, request, Response

from flask_cors import CORS

app = Flask('app')
CORS(app)


def get_json(url):
    r = requests.get(url, auth=(request.authorization['username'], request.authorization['password']))
    r.raise_for_status()
    return r.json()

def get_items():
    items = get_json('https://myopenhab.org/rest/items/')
    items = [entry['name'] for entry in items if entry['type'] != 'Group']
    return items

def to_number(state):
    try:
        return float(state)
    except ValueError:
        return {'CLOSED': 0, 'OPEN': 1}[state]
    
@app.route('/')
def index():    
    print(request.__dict__)
    print(request.json)
    try:
        get_json('https://myopenhab.org/rest/') # raises on HTTP 401
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return Response('Unauthorized', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
        else:
            raise
    return 'OK'

@app.route('/search', methods=['POST', 'GET'])
def grafana_search():
    print(request.json)
    return json.dumps(get_items())

def get_series(item, start, end):
    data = get_json(f'https://myopenhab.org/rest/persistence/items/{item}?starttime={start}&endtime={end}')
    df = pd.DataFrame.from_dict(data['data'])
    df.index = pd.to_datetime(df.pop('time'), unit='ms', utc=True)
    df = df['state'].apply(to_number)
    df.name = item
    return df

def resample(series, freq):
    return series.resample(rule=freq, label='right', closed='right').mean()

def _series_to_simple_json(series, target):
    if not len(series):
        return {'target': '%s' % (target),
                'datapoints': []}

    sorted_series = series.dropna().sort_index()
    timestamps = sorted_series.index.to_numpy('datetime64[ms]').astype(np.int64).tolist()
    values = sorted_series.values.tolist()

    return {'target': sorted_series.name,
            'datapoints': list(zip(values, timestamps))}

@app.route('/query', methods=['POST'])
def grafana_query():
    print(request.json)
    start, end = request.json['range']['from'], request.json['range']['to']
    targets = [entry['target'] for entry in request.json['targets']]
    if 'intervalMs' in request.json:
        freq = str(request.json.get('intervalMs')) + 'ms'
    else:
        freq = None
    
    # only supporting 'timeserie'
    out = []
    for target in targets:
        entry = _series_to_simple_json(resample(get_series(target, start, end), freq), target)
        out.append(entry)
    return json.dumps(out)

app.run(debug=False)