import time

from flask import (
    Blueprint, g, jsonify, redirect, request, url_for
)

from casebook.auth import login_required
from casebook.db.db import get_full_db_connection
from casebook.objects.postobject import PostObject

bp = Blueprint('posts', __name__, url_prefix='/api')

@bp.route('/posts') @login_required
def posts():
    try:
        username = request.args.get("username")
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT post.id, users.username, unix_timestamp(post.posted_time), post.title, post.body FROM post, users WHERE post.author_id = users.id AND users.username = %(username)s", {'username': username}) 
        rows = cursor.fetchall()
    except:
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    data = map(lambda x: PostObject(x).to_dict(), rows)
    
    return jsonify(posts=list(data))

@bp.route('/post', methods=['POST'])
@login_required
def post():
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()) 
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO post(author_id, posted_time, title, body) VALUES (%s, %s, %s, %s)", (g.user_id, timestamp, request.form['title'], request.form['body'])) 
        conn.commit()
    except:
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    return ('', 204)

@bp.route('/deletepost', methods=['DELETE'])
@login_required
def delete_post():
    try:
        post_id = request.form['post_id']
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM post WHERE post.id = %s AND post.author_id = %s", (post_id, g.user_id))
        conn.commit()
    except:
        return ('', 401)
    finally: 
        cursor.close()
        conn.close()
    
    return ('', 204)

@bp.route('/updatepost', methods=['PUT'])
@login_required
def update_post():
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()) 
        conn = get_full_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE post SET post.posted_time = %s, post.title = %s, post.body = %s WHERE post.id = %s AND post.author_id = %s", (timestamp, request.form['title'], request.form['body'], request.form['id'], g.user_id))
        conn.commit()
    except:
        return ('', 401)
    finally:
        cursor.close()
        conn.close()

    return('', 204)
