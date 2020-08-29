import logging
import os
import re

from flask import Flask, redirect, render_template, request, session, url_for, jsonify

from attestation import Blake2Attestation
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken

logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)
app.config.from_json('config.json')
app.config['SECRET_KEY'] = os.urandom(16)
app.config.update(dict(
  PREFERRED_URL_SCHEME = 'https'
))
oauth = OAuth(app)
oauth.register('jaccount')

attestation = Blake2Attestation(secret=bytes.fromhex(
    app.config.get('ATTESTATION_SECRET')))

qq_pattern = re.compile(r'^[1-9]\d{4,}')


def check_qq(qq: str) -> bool:
    return True if qq_pattern.fullmatch(qq) else False


@app.before_request
def login_required():
    if request.path not in [url_for('cover_page'), url_for('generate')]:
        return None

    if 'user' not in session:
        if request.path == url_for('generate'):
            return 'Please login first', 401
        else:
            return redirect(url_for('login'))


@app.route('/')
def cover_page():
    return render_template('index.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.jaccount.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.jaccount.authorize_access_token()

    # resp = oauth.jaccount.get('/v1/me/profile', token=token)
    # print(json.dumps(resp.json(), ensure_ascii=False, indent=True))

    claims = jwt.decode(token.get('id_token'),
                        oauth.jaccount.client_secret,
                        claims_cls=CodeIDToken)
    claims.validate()
    session['user'] = claims

    return redirect(url_for('cover_page'))


@app.route('/generate', methods=['POST'])
def generate():
    qq = request.form.get('qq_number', type=str, default='')
    if check_qq(qq):
        try:
            return attestation.generate(qq)
        except Exception as e:
            return str(e), 500
    else:
        return '填写错误，请输入正确的QQ号', 400


@app.route('/verify', methods=['POST'])
def verify():
    qq = request.json.get('qq_number')
    token = request.json.get('token')

    if qq == None or token == None:
        return jsonify({
            "success": False,
            "message": "Compulsory parameters lost"
        }), 400

    if not check_qq(qq):
        return jsonify({
            "success": False,
            "message": "Invalid QQ number"
        }), 400

    try:
        timestamp = attestation.verify(qq, token)
        if timestamp == None:
            return jsonify({
                "success": False,
                "message": "Verification Failed"
            })
        else:
            return jsonify({
                "success": True,
                "message": timestamp.isoformat()
            })
    except (UnicodeEncodeError, ValueError) as e:
        return jsonify({
            "success": False,
            "message": "Invalid token"
        }), 400


if __name__ == '__main__':
    app.run()
