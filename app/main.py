from flask import Flask, render_template, request, redirect, session, url_for

import sys
import os
import requests

#######initialize Flask application#######
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
##########################################

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@app.route("/about", methods=['POST'])
def about():
    if request.method == 'POST':
        info_text = """I used machine learning clustering to group together the most similar tracks in
        the top 50 charts of the US, UK and World on Spotify. In order to create these playlists, you will need
        to input a certain minimum number of songs. This is for the algorithm to use a base number and build
        clusters."""
        return render_template('create.html', info_text=info_text)

@app.route("/playlists", methods=['GET', 'POST'])
def playlists():
    if request.method == 'GET':
        return f"""This url is not available unless you have requested to create playlists. Visit '/create' to start."""
    elif request.method == 'POST':
        form_data = request.form
        return render_template('playlists.html', form_data=form_data['minimum number of songs per playlist'])

@app.route("/login", methods=['GET', 'POST'])
def login():
    return f"""Currently under construction. Check back soon for updates."""


if __name__ == "__main__":
    app.run(debug=True)
