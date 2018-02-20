from app import app

from flask import render_template, request
from flask_material import Material
from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import Required
import sys
import pandas as pd

Material(app)


class ExampleForm(Form):
    search = TextField(
        'Search Field', description='Origin or Destination')


def search_dat(file_name, search_term):
    # search the dataset for a query

    df = pd.read_csv(file_name)
    return df[df['Address'].str.contains(search_term, case=False) |
              df['City'].str.contains(search_term, case=False) |
              df['State'].str.contains(search_term, case=False)].values.tolist()


def get_top_origins(file_name):
    df = pd.read_csv(file_name)
    return df['City'].value_counts().index.values.tolist()[0:4]


@app.route('/')
def index():
    data_file_name = 'app/met_gala_attendees.csv'
    form = ExampleForm()

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

@app.route('/login')
def login():
    return render_template('login.html',
                            title = 'ORF 401: Lab 2 - Login')
