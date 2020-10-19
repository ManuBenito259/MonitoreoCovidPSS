from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.auth import uploader_login_required
from flaskr.database.db import get_db

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=('GET', 'POST'))
@uploader_login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO cargaDiaria (id, centroSalud, fecha, respDisp, respOc, camaUTIDisp, camaUTIOc, camaGCDisp, camaGCOc)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], title, str(date.today()) , body, "5", "6", "7", "8", "9") #TODO: placeholder
            )
            db.commit()
            return redirect(url_for('upload.upload'))

    return render_template('uploader/upload.html')