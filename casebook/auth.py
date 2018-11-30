import functools

from flask import (
    Blueprint, g
)


bp = Blueprint('auth', __name__, url_prefix='/api')

def login_required(view):
    @functools.wrap(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

