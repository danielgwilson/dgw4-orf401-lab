from flask import Flask, render_template
from flask_material import Material
from flask_wtf import Form
from wtforms import TextField

app = Flask(__name__)
Material(app)

@app.route('/')
def hello_world():
    return render_template('index.html', title='ORF 401: Lab 1 - Python')
