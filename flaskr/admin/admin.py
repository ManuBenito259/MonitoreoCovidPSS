import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=('GET', 'POST'))
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM admin WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('admin.admin_index'))

        flash(error)

    return render_template('admin/login.html')


@bp.route('/index')
def admin_index():
    db = get_db()
    read_users = db.execute(
        'SELECT *'
        ' FROM user'
        ' ORDER BY id DESC'
    ).fetchall()

    #read_users = db.execute(
    #    'SELECT dni, nombre, apellido, jurisdiccion'
    #    ' FROM usuarioLector'
    #    ' ORDER BY apellido DESC'
    #).fetchall()

    write_users = db.execute(
        'SELECT dni, nombre, apellido, centroSalud'
        ' FROM usuarioCarga'
        ' ORDER BY apellido DESC'
    ).fetchall()

    admins = db.execute(
        'SELECT id, username'
        ' FROM admin'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('admin/index.html', read_users=read_users)




