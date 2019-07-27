from flask import render_template, redirect, flash, jsonify
from . import app

@app.route('/')
def index():
    return render_template('index.html')