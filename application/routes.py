from flask import render_template, redirect, flash, jsonify
from . import app

import json

MAPPING = {}
with open('db/mapping.json', 'r') as f:
    MAPPING = json.load(f)

MATERIALS = []
with open('db/materials.json', 'r') as f:
    MATERIALS = json.load(f)

@app.route('/')
def index():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    attentions = []
    for a in petya['attention']:
        tmp = a.split(';')
        attentions.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    petya['attention_strings'] = attentions
    favorite = []
    for f in petya['attention']:
        tmp = f.split(';')
        favorite.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    petya['favorite_strings'] = favorite
    return render_template('index.html', petya=petya)


@app.route('/api/attentions/')
def attentions():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    attentions = []
    for a in petya['attention']:
        tmp = a.split(';')
        attentions.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    return jsonify({
        'attentions': attentions
    })

@app.route('/api/favorites/')
def favorites():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    favorites = []
    for a in petya['favorite']:
        tmp = a.split(';')
        favorites.append(MAPPING[str(len(tmp)-1)][str(tmp[-1])])
    return jsonify({
        'favorites': favorites
    })

@app.route('/api/cards_favorites/')
def cards_favorite():
    return jsonify({
        'cards_favorites': []
    })

@app.route('/api/cards_attentions/')
def cards_attention():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    attention = []
    for a in petya['attention']:
        for mat in MATERIALS:
            if a in mat['kes']:
                attention.append({mat['name']: {"type": mat['type']}})
    return jsonify({
        'attention': attention
    })