from flask import render_template, redirect, flash, jsonify
from . import app

import json
import pandas as pd

MAPPING = {}
with open('db/mapping.json', 'r') as f:
    MAPPING = json.load(f)

MATERIALS = pd.read_csv('db/materials.csv', sep=',')
# print(MATERIALS.iloc[1])

HOST = 'https://uchebnik.mos.ru/cms/api'

@app.route('/')
def index():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    return render_template('index.html', petya=petya)


@app.route('/api/attentions/')
def attentions():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    attentions = []
    for a in petya['attentions']:
        key = a.split('.')[0]
        attentions.append(MAPPING[key])
    attentions = list(set(attentions))
    return jsonify({
        'attentions': attentions
    })

@app.route('/api/favorites/')
def favorites():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    favorites = []
    for f in petya['favorites']:
        key = f.split('.')[0]
        favorites.append(MAPPING[key])
    favorites = list(set(favorites))
    return jsonify({
        'favorites': favorites
    })

@app.route('/api/cards_favorites/')
def cards_favorite():
    return jsonify({
        'cards_favorites': []
    })

@app.route('/api/cards_attentions/')
def cards_attentions():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    cards_attentions = []
    for a in petya['attentions']:
        for i in range(len(MATERIALS)):
            if a == MATERIALS.iloc[i]['kes']:
                cards_attentions.append({
                    'title': MATERIALS.iloc[i]['name'],
                    'type': 'Книга',
                    'id': str(int(MATERIALS.iloc[i]['book_id'])),
                    # 'description': MATERIALS.iloc[i]['description'],
                    'author': MATERIALS.iloc[i]['authors'],
                    'img-src': HOST + MATERIALS.iloc[i]['cover']
                })
    print(cards_attentions)
    return jsonify({
        'cards_attentions': cards_attentions
    })