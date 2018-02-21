from app import app
from app import db
from app.forms import LoginForm, SearchForm, RegistrationForm

# login stuff
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User

from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse
from flask_material import Material

import sys
import pandas as pd
import numpy as np

Material(app)


def search_dat(file_name, search_term):
    # search the dataset for a query

    df = pd.read_csv(file_name)
    # results = df[df['Address'].str.contains(search_term, case=False) |
    #           df['City'].str.contains(search_term, case=False) |
    #           df['State'].str.contains(search_term, case=False)].values.tolist()

    # Only search city now since we're looking for people from the same origin City
    # later this can be converted to closest by GIS location
    results = df[df['City'].str.contains(search_term, case=False)].sample(n=1).values.tolist()
    return results


def get_top_origins(file_name):
    df = pd.read_csv(file_name)
    return df['City'].value_counts().index.values.tolist()[0:4]


@app.route('/')
def index():
    data_file_name = 'app/met_gala_attendees.csv'
    form = SearchForm()

    # if there was a query entered, build a table
    query = ''
    results = None
    if request.args:
        if request.args['search'] != '':
            query = request.args['search']
            results = search_dat(data_file_name, query)

    # make chips out of the top 4 cities
    chips = get_top_origins(data_file_name)

    return render_template('index.html',
                           title='ORF 401: Lab 2',
                           form=form,
                           query=query,
                           results=results,
                           chips=chips)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html',
                           title='ORF 401: Lab 2 - Login',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    print('test')
    form = RegistrationForm()
    if form.validate_on_submit():
        print('test2')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='ORF 401: Lab 2 - Register', form=form)
