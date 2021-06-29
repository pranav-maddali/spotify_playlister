from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_login import login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

from app.curate import *
from app import application
from app.models import User
from app import db
import config

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
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')

        #'Remember me' implementation
        if request.form.get('remember'):
            remember_user = True
        else:
            remember_user = False

        curr_user = User.query.filter_by(email=email).first()

        #check if the email exists in the database and then if the password matches
        if curr_user is None or not check_password_hash(curr_user.password, pw):
            flash("The username or password do not match. Please check your credentials and try again.")
            return redirect(url_for('login'))

        login_user(curr_user, remember=remember_user)
        return redirect(url_for('home'))

@application.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        pw = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        #check if the user already exists
        if user is not None:
            flash("This email already exists. Redirecting to login page.")
            return redirect(url_for('login'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(pw,method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
