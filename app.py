from flask import Flask, render_template, request
from flask_material import Material
from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import Required
import sys
import pandas as pd

app = Flask(__name__)
Material(app)


class ExampleForm(Form):
    search = TextField(
        'Search Field', description='Origin or Destination')


def search_dat(file_name, search_term):
    # rides = []

    file = pd.read_csv(file_name)

    # for row in file[file['City'].str.contains(search_term, case=False)].values.tolist():
    #     rides.append(' '.join(str(s) for s in row))

    return file[file['City'].str.contains(search_term, case=False)].values.tolist()


@app.route('/')
def index():
    form = ExampleForm(csrf_enabled = False)
    if request.args:
        if request.args['search'] != '':
            query = request.args['search']
            results = search_dat('met_gala_attendees.csv', query)
            return render_template('index_mdl.html',
                                    title='ORF 401: Lab 1 - Python',
                                    form=form,
                                    results=results)

    return render_template('index_mdl.html', title='ORF 401: Lab 1 - Python', form=form)


if __name__ == '__main__':
    app.run(debug=True)
