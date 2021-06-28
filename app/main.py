from flask import Flask, Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_required, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from curate import *

import sys
import os
import json
import requests

##########################################
app = Flask(__name__)
##########################################

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    info_text = """I used machine learning clustering to group together the most similar tracks in
    the top 50 charts of the US, UK and World on Spotify. In order to create these playlists, you will need
    to input a certain minimum number of songs. This is for the algorithm to use a base number and build
    clusters."""
    if request.method == 'POST':
        return render_template('create.html', info_text=info_text)
    elif request.method == 'GET':
        return render_template('create.html', info_text=info_text)

@app.route("/playlists", methods=['GET', 'POST'])
def playlists():
    if request.method == 'GET':
        return f"""This url is not available unless you have requested to create playlists. Visit '/create' to start."""
    elif request.method == 'POST':
        form_data = request.form

        res = create_playlists(int(form_data['minimum number of songs per playlist']))

        return render_template('playlists.html', form_data=form_data['minimum number of songs per playlist'], data=res.to_html())


@app.route("/login", methods=['GET', 'POST'])
def login():
    return f"""Currently under construction. Check back soon for updates."""


if __name__ == "__main__":
    app.run(debug=True)
