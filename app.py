from flask import Flask, render_template
from flask_material import Material
from flask_wtf import Form
from wtforms import TextField

app = Flask(__name__)
Material(app)

class ExampleForm(Form):
    field1 = TextField('Search Field', description='Enter an origin or a destination')
    submit_button = SubmitField('Submit Form')

@app.route('/')
def hello_world():
    form = ExampleForm()
    return render_template('index.html', title='ORF 401: Lab 1 - Python', form = form)
