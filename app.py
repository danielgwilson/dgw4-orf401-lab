from flask import Flask, render_template, request
from flask_material import Material
from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import Required
import sys
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Material(app)


class ExampleForm(Form):
    search = TextField(
        'Search Field',
        description='Enter an origin or a destination')


def search_dat(file_name, search_term):
    rides = []

    with open(file_name, "r") as file:
        for line in file:
            name, source, dest, date, time, multiple, num = line.split(
                "\t")

            if search_term in source or search_term in dest:
                rides.append(name + " " + source + " " + dest + " " + date + \
                    " " + time + " " + multiple + " " + num)

    return rides


@app.route('/')
def index():
    form = ExampleForm()
    if request.args:
        query = request.args['search']
        results = search_dat('riders.dat', query)
        return render_template('index.html',
                                title='ORF 401: Lab 1 - Python',
                                form=form,
                                results=results)
    return render_template('index.html', title='ORF 401: Lab 1 - Python', form=form)

if __name__ == '__main__':
    app.run(debug=True)
