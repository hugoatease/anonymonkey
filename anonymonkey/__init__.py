from flask import Flask, render_template, session, redirect, request
from anonymonkey.api import api
from .schemas import db
import requests
from urllib import urlencode
import cryptography.hazmat.primitives.serialization
from cryptography.hazmat.backends import default_backend
import jwt
from flask_login import login_user, current_user
from .auth import login_manager
from .schemas import User
from .auth import UserHandler
import json

app = Flask(__name__)
app.config.from_object('settings')
app.config['MONGODB_SETTINGS'] = {
    'host': app.config['MONGODB_HOST'],
    'port': app.config['MONGODB_PORT'],
    'db': app.config['MONGODB_DB'],
    'tz_aware': True
}

login_manager.init_app(app)
db.init_app(app)
api.init_app(app)


@app.route('/')
def index():
    params = {}
    if current_user.is_authenticated:
        params['user'] = current_user.serialize()
        params['authenticated'] = True
    else:
        params['authenticated'] = False
    return render_template('index.html', params=json.dumps(params))


@app.route('/<path:path>')
def index_all(path):
    params = {}
    if current_user.is_authenticated:
        params['user'] = current_user.serialize()
        params['authenticated'] = True
    else:
        params['authenticated'] = False
    return render_template('index.html', params=json.dumps(params))


@app.route('/login')
def login():
    params = {
        'scope': 'openid profile email',
        'response_type': 'code',
        'client_id': app.config['OPENID_CLIENT'],
        'redirect_uri': app.config['OPENID_REDIRECT']
    }

    if 'signup_redirect' in request.args:
        params['signup_redirect'] = 'true'

    params = urlencode(params)

    if 'next' in request.args:
        session['login_next'] = request.args['next']

    return redirect(app.config['OPENID_AUTHORIZE_ENDPOINT'] + '?' + params)


@app.route('/login/return')
def login_return():
    code = request.args['code']
    clientAuth = requests.auth.HTTPBasicAuth(app.config['OPENID_CLIENT'], app.config['OPENID_SECRET'])
    tokens = requests.post(app.config['OPENID_TOKEN_ENDPOINT'], auth=clientAuth, data={
        'grant_type': 'authorization_code',
        'redirect_uri': app.config['OPENID_REDIRECT'],
        'code': code
    }).json()

    key = cryptography.hazmat.primitives.serialization.load_pem_public_key(app.config['OPENID_ISSUER_KEY'], backend=default_backend())

    sub = jwt.decode(tokens['id_token'], key, audience=app.config['OPENID_CLIENT'])['sub']
    info = requests.get(app.config['OPENID_USERINFO_ENDPOINT'], headers={'Authorization': 'Bearer ' + tokens['access_token']}).json()

    if User.objects.with_id(sub) is None:
        user = User(
            sub=sub,
            email=info['email'],
            first_name=info['given_name'],
            last_name=info['family_name'],
            id_token=tokens['id_token']
        )
        user.save()
    else:
        user = User.objects.with_id(sub)
        user.id_token = tokens['id_token']
        user.email = info['email']
        user.first_name = info['given_name']
        user.last_name = info['family_name']
        user.save()

    login_user(UserHandler(user))

    if 'login_next' not in session:
        return redirect('/')
    else:
        return redirect(session['login_next'])