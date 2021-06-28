from flask import Flask, Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_required, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from app.curate import *
from app import application

import sys
import os
import json
import requests

@application.route("/")
@application.route("/home")
def home():
    return render_template('home.html')

@application.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@application.route("/about", methods=['GET', 'POST'])
def about():
    info_text = """I used machine learning clustering to group together the most similar tracks in
    the top 50 charts of the US, UK and World on Spotify. In order to create these playlists, you will need
    to input a certain minimum number of songs (1-19). This is for the algorithm to use a base number and build
    clusters."""
    if request.method == 'POST':
        return render_template('create.html', info_text=info_text)
    elif request.method == 'GET':
        return render_template('create.html', info_text=info_text)

@application.route("/playlists", methods=['GET', 'POST'])
def playlists():
    global track_ids
    if request.method == 'GET':
        return f"""This url is not available unless you have requested to create playlists. Visit '/create' to start."""
    elif request.method == 'POST':
        form_data = request.form
        res, clusters = create_playlists(int(form_data['minimum number of songs per playlist']))

        track_ids, res = res['id'], res.drop('id', 1)

        return render_template('playlists.html', form_data=form_data['minimum number of songs per playlist'], data=res.to_html(), num=clusters)


@application.route("/login", methods=['GET', 'POST'])
def login():
    return f"""Currently under construction. Check back soon for updates."""
