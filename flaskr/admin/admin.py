from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import admin_login_required
from flaskr.database.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')




@bp.route('/index')
@admin_login_required
def admin_index():
    db = get_db()
    users = db.execute(
        'SELECT *'
        ' FROM users'
    ).fetchall()


    return render_template('admin/index.html', users=users)


@bp.route('/register_uploader', methods=('GET', 'POST'))
@admin_login_required
def uploaderRegister():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (username, password, type) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), "uploader")
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/uploader_register.html')

@bp.route('/register_viewer', methods=('GET', 'POST'))
@admin_login_required
def viewerRegister():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (username, password, type) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), "viewer")
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/viewer_register.html')

@bp.route('/register_admin', methods=('GET', 'POST'))
@admin_login_required
def adminRegister():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (username, password, type) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), "admin")
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/viewer_register.html')

