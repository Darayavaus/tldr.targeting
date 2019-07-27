from flask import render_template, redirect, flash, jsonify
from . import app

import json

MAPPING = {}
with open('db/mapping.json', 'r') as f:
    MAPPING = json.load(f)

@app.route('/')
def index():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    attention = []
    for a in petya['attention']:
        attention.append(MAPPING['2'][str(a.split(';')[-1])])
    petya['attention_strings'] = attention
    return render_template('index.html', petya=petya)