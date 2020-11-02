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

    return render_template('admin/admin_register.html')


@bp.route('/upload_location', methods=('GET', 'POST'))
@admin_login_required
def uploadLocation():
    if request.method == 'POST':
        cp = request.form['codigoPostal']
        provincia = request.form['provincia']
        ciudad = request.form['ciudad']
        db = get_db()
        error = None

        if not cp:
            error = 'Ingrese el Codigo Postal.'
        elif not provincia:
            error = 'Ingrese la provincia.'
        elif not ciudad:
            error = 'Ingrese el nombre de la ciudad'
        elif db.execute(
                'SELECT cp FROM ubicacion WHERE cp = ?', (cp,)
        ).fetchone() is not None:
            error = 'El codigo postal {} ya existe.'.format(cp)

        if error is None:
            db.execute(
                'INSERT INTO ubicacion (cp, provincia, ciudad) VALUES (?, ?, ?)',
                (cp, provincia, ciudad)
            )
            db.commit()
            return redirect(url_for('admin.locations'))

        flash(error)

    return render_template('admin/upload_location.html')


@bp.route('/locations')
@admin_login_required
def locations():
    db = get_db()
    ubicaciones = db.execute(
        'SELECT *'
        ' FROM ubicacion'
    ).fetchall()
    print(len(ubicaciones))

    return render_template('admin/ubicaciones.html', ubicaciones=ubicaciones)
