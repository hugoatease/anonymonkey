from flask import Flask, render_template
from anonymonkey.api import api
from .schemas import db

app = Flask(__name__)
app.config.from_object('settings')
app.config['MONGODB_SETTINGS'] = {
    'host': app.config['MONGODB_HOST'],
    'port': app.config['MONGODB_PORT'],
    'db': app.config['MONGODB_DB'],
    'tz_aware': True
}

db.init_app(app)
api.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def index_all(path):
    return render_template('index.html')
