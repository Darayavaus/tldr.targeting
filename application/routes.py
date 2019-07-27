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
        tmp = a.split(';')
        attention.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    petya['attention_strings'] = attention
    favorite = []
    for f in petya['attention']:
        tmp = f.split(';')
        favorite.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    petya['favorite_strings'] = favorite
    return render_template('index.html', petya=petya)