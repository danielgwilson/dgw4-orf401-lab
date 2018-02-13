from flask import Flask
from flask import render_template
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates/')

app = Flask(__name__, template_folder=template_path)

@app.route('/')
def hello_world():
    return render_template('index.html', title='ORF 401: Assignment #1 - Python')
