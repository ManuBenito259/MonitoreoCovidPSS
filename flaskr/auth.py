import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/viewer', methods=('GET', 'POST'))
def viewer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND type = ?', (username, "viewer")
        ).fetchone()

        if (user is None) or (not check_password_hash(user['password'], password)):
            error = 'La contraseña y/o nombre de usuario es incorrecto'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('data.index'))

        flash(error)

    return render_template('auth/viewer_login.html')


@bp.route('/uploader', methods=('GET', 'POST'))
def uploader_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND type = ?', (username, "uploader")
        ).fetchone()

        if (user is None): #or (not check_password_hash(user['password'], password)):
            error = 'La contraseña y/o nombre de usuario es incorrecto'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('upload.index'))

        flash(error)

    return render_template('auth/uploader_login.html')


@bp.route('/admin', methods=('GET', 'POST'))
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND type = ?', (username, "admin")
        ).fetchone()

        if (user is None) or (not check_password_hash(user['password'], password)):
            error = 'La contraseña y/o nombre de usuario es incorrecto'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('auth/admin_login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()







@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def viewer_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.viewer_login'))
        if g.user['type'] != "viewer":
            return redirect(url_for('auth.viewer_login'))
        return view(**kwargs)

    return wrapped_view


def uploader_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.uploader_login'))
        if g.user['type'] != "uploader":
            return redirect(url_for('auth.uploader_login'))
        return view(**kwargs)

    return wrapped_view

def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.admin_login'))
        if g.user['type'] != "admin":
            return redirect(url_for('auth.admin_login'))
        return view(**kwargs)

    return wrapped_view