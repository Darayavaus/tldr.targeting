from flask import render_template, redirect, flash, jsonify
from . import app

import json
import pandas as pd

MAPPING = pd.read_csv('db/kess_index.csv', sep=';')

MATERIALS = pd.read_csv('db/lesson_templates.csv', sep=';')

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
    MAPPING = pd.read_csv('db/kess_index.csv', sep=';')
    print(MAPPING.iloc[1])
    for a in petya['attentions']:
        attentions.append(
            list(MAPPING[MAPPING['kesId']==a][['subjectName', 'kesName']].values[0])
        )
    return jsonify({
        'attentions': attentions
    })

@app.route('/api/favorites/')
def favorites():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    favorites = []
    for f in petya['favorites']:
        favorites.append(
            list(MAPPING[MAPPING['kesId']==f][['subjectName', 'kesName']].values[0])
        )
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
            if str(a) in ''.join(MATERIALS.iloc[i]['controllable_item_ids']):
                cards_attentions.append({
                    'title': MATERIALS.iloc[i]['topic_name'],
                    'type': 'Шаблон лекции',
                    'level': 'Базовый' if MATERIALS.iloc[i]['studying_level_id']==1 else 'Углубленный',
                    'description': MATERIALS.iloc[i]['description'],
                    'author': MATERIALS.iloc[i]['author_name']
                })
    return jsonify({
        'cards_attentions': cards_attentions
    })