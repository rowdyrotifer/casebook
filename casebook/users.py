from flask import (
    Blueprint, g, jsonify, url_for, request
)

from casebook.auth import login_required
from casebook.db.db import get_full_db_connection


bp = Blueprint('users', __name__, url_prefix='/api')

@bp.route('/get_following')
@login_required
def get_following():
    try:
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT users.username FROM users, follow WHERE follow.follower_id = %(user_id)s AND users.id = following_id", {'user_id': g.user_id})
        rows = cursor.fetchall()
    except:
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    usernames = map(lambda x: x[0], rows)

    return jsonify(following=list(usernames))

@bp.route('/users')
@login_required
def users():
    try:
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT users.username FROM users")
        rows = cursor.fetchall()
    except:
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    usernames = map(lambda x: x[0], rows)

    return jsonify(users=list(usernames))

@bp.route('/follow', methods=['POST'])
@login_required
def follow():
    followed_username = request.form['username']
    try:
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO follow (following_id, follower_id) VALUES ((SELECT users.id FROM users WHERE users.username = %s), %s)", (followed_username, g.user_id))
        conn.commit()
    except Exception as e:
        print(e)
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    return ('', 204)

@bp.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    unfollowed_username = request.form['username']
    try:
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM follow WHERE follow.follower_id = %s AND follow.following_id = (SELECT users.id FROM users WHERE users.username = %s)", (g.user_id, unfollowed_username))
        conn.commit()
    except Exception as e:
        print(e)
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    return ('', 204)
