import string
from datetime import datetime, timedelta
import random

import bcrypt
import functools

from flask import (
    Blueprint, g,
    redirect, url_for, request, session, jsonify, flash, make_response)
from gunicorn import app

from casebook.db.db import get_full_db_connection

bp = Blueprint('auth', __name__, url_prefix='/api')


def validate_token(token):
    conn = get_full_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM session WHERE token = %s', (token,))
    result = cursor.fetchone()
    if result is None:
        return None
    token, user_id, expiration_time = result
    if expiration_time >= datetime.now():
        return user_id
    else:
        return None


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        error_response = make_response()
        error_response.status_code = 401
        if 'token' not in request.cookies:
            return error_response
        else:
            token = request.cookies['token']
            validated_user_id = validate_token(token)
            if validated_user_id is not None:
                g.user_id = validated_user_id
            else:
                return error_response
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
    username = request.form['username']
    password = request.form['password']
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

    return jsonify({'result': 'success'})

def generate_user(conn, username, password):
    salt = bcrypt.gensalt()
    password_bcrypt = bcrypt.hashpw(password.encode('utf8'), salt)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password_bcrypt))
    conn.commit()

@bp.route('/makeuser', methods=['POST'])
def makeuser():
    username = request.form['username']
    password = request.form['password']
    conn = get_full_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE username = %s', (username,))
    if len(cursor.fetchall()) > 0:
        return jsonify({'result': 'exists'})
    else:
        generate_user(conn, username, password)
        return jsonify({'result': 'success'})


@bp.route('/deleteuser', methods=['POST'])
@login_required
def deleteuser():
    conn = get_full_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (g.user_id,))
    conn.commit()
    return '', 200
