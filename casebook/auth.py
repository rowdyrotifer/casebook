import functools

from flask import (
    Blueprint, g, redirect, url_for
)


bp = Blueprint('auth', __name__, url_prefix='/api')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

