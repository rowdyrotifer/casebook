import string
from datetime import datetime, timedelta
import random

import bcrypt
import functools

from flask import (
    Blueprint, g,
    redirect, url_for, request, session, jsonify, flash, make_response)

from casebook.db.db import get_full_db_connection

bp = Blueprint('auth', __name__, url_prefix='/api')


def validate_token(conn, token):
    result = conn.execute('SELECT * FROM session WHERE token = %(token_value)', {'token_value': token}).fetchone()
    if result is None:
        return None
    token, user_id, expiration_time = result
    if expiration_time < datetime.now():
        return user_id
    else:
        return None


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'token' not in request.cookies:
            return redirect('/api/login')
        else:
            token = request.cookies['token']
            validated_user_id = validate_token(token)
            if validated_user_id is not None:
                g.user_id = validated_user_id
            else:
                redirect('/api/login')
            return view(**kwargs)

    return wrapped_view


def check_password_hash(password_bcrypt, password):
    return password_bcrypt == bcrypt.hashpw(password.encode('utf8'), password_bcrypt)


def generate_session(conn, user_id):
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
    token = ''.join(random.SystemRandom().choice(charset) for _ in range(32))
    exp_time = datetime.now() + timedelta(hours=24)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO session(token, user_id, expiration_time) VALUES (%s, %s, %s)", (token, user_id, exp_time))
    conn.commit()
    return token


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.args['username']
        password = request.args['password']
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user is not None and check_password_hash(user[2], password):
            token = generate_session(conn, user[0])
            resp = make_response(jsonify({'result': 'success', 'token': token}))
            resp.set_cookie('token', token)
            return resp
        else:
            return jsonify({'result': 'failure'})

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return jsonify({'result': 'success'})

        flash(error)

    return 405
