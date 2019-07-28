from flask import render_template, redirect, flash, jsonify
from . import app

import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KDTree
import numpy as np

MAPPING = {}
with open('db/mapping.json', 'r') as f:
    MAPPING = json.load(f)

MATERIALS = pd.read_csv('db/materials.csv', sep=',')

df_kes = MATERIALS[['kes1', 'kes2', 'kes3']]
enc = OneHotEncoder(sparse=False)
enc.fit(df_kes)
df_train = pd.DataFrame(enc.transform(df_kes).astype(int))
df_train[['authors', 'book_id', 'cover', 'subject', 'name']] = MATERIALS[['authors', 'book_id', 'cover', 'subject', 'name']]
neighbors = df_train[df_train.columns[0:71]]
kdt = KDTree(neighbors, leaf_size=30, metric='euclidean')

def get_vector(xs):
    arr = [int(x) for x in xs]
    return enc.transform(np.array(arr).reshape(1, len(arr)))

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
        key = a.split('d')[0]
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
    fav_indexes = []
    for f in petya['favorites']:
        key = f.split('d')[0]
        fav_indexes.append(f)
        favorites.append(MAPPING[key])
    favorites = list(set(favorites))
    return jsonify({
        'favorites': {'names' : favorites, "indexes": fav_indexes}
    })

@app.route('/api/cards_favorites/<fav>')
def cards_favorite(fav='41d4d104'):
    fav_indexes = [f.split('d') for f in fav.split('c')]
    print(fav_indexes)
    cards_favorites = []
    fav_vector = np.array([0]*71, dtype=int)
    for f in fav_indexes:
        fav_vector = np.logical_or(fav_vector, get_vector(f)).astype(int)
        print(fav_vector)
    dists, recomends = kdt.query(fav_vector, 3)
    print(MATERIALS.iloc[recomends[0]])
    for d, i in zip(dists[0], recomends[0]):
        print(d, i)
        if d < 2:
            cards_favorites.append({
                'title': MATERIALS.iloc[i]['name'],
                'type': 'Книга',
                'id': str(int(MATERIALS.iloc[i]['book_id'])),
                # 'description': MATERIALS.iloc[i]['description'],
                'author': MATERIALS.iloc[i]['authors'],
                'imgSrc': HOST + MATERIALS.iloc[i]['cover'],
                'theme': MAPPING[MATERIALS.iloc[i]['kes'].split('.')[0]],
                'kes': MATERIALS.iloc[i]['kes'],
            })
    return jsonify({
        'cards_favorites': cards_favorites
    })

@app.route('/api/cards_attentions/')
def cards_attentions():
    with open('db/petya.json', 'r') as f:
        petya = json.load(f)
    cards_attentions = []
    for a in petya['attentions']:
        for i in range(len(MATERIALS)):
            if a.replace('d', '.') == MATERIALS.iloc[i]['kes']:
                cards_attentions.append({
                    'title': MATERIALS.iloc[i]['name'],
                    'type': 'Книга',
                    'id': str(int(MATERIALS.iloc[i]['book_id'])),
                    # 'description': MATERIALS.iloc[i]['description'],
                    'author': MATERIALS.iloc[i]['authors'],
                    'imgSrc': HOST + MATERIALS.iloc[i]['cover'],
                    'theme': MAPPING[MATERIALS.iloc[i]['kes'].split('.')[0]],
                    'kes': MATERIALS.iloc[i]['kes'].resplace('.', 'd'),
                })
    print(cards_attentions)
    return jsonify({
        'cards_attentions': cards_attentions
    })