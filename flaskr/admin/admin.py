from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')




@bp.route('/index')
def admin_index():
    db = get_db()
    uploader_users = db.execute(
        'SELECT *'
        ' FROM uploader_user'
    ).fetchall()

    read_users = db.execute(
        'SELECT *'
        ' FROM viewer_user'
    ).fetchall()

    admins = db.execute(
        'SELECT *'
        ' FROM admin'
    ).fetchall()

    return render_template('admin/index.html', read_users=read_users)


@bp.route('/register_uploader', methods=('GET', 'POST'))
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
                'SELECT id FROM uploader_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO uploader_user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/uploader_register.html')

@bp.route('/register_viewer', methods=('GET', 'POST'))
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
                'SELECT id FROM viewer_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO viewer_user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/viewer_register.html')

@bp.route('/register_admin', methods=('GET', 'POST'))
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
                'SELECT id FROM admin WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO admin (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/viewer_register.html')

