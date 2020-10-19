import os
import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import datetime
from werkzeug.utils import secure_filename

from flaskr.auth import uploader_login_required
from flaskr.database.db import get_db


bp = Blueprint('upload', __name__, url_prefix='/upload')
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}
DEFAULT_NAME="PlanillaExterna.xlsx"


def storeData(file):
    df = pd.read_excel(file, 'Sheet1')
    db = get_db()
    rows = df.shape[0]  # obtiene el numero de filas (sin contar el encabezado)

    for i in range(rows):
        lista = df.loc[i].tolist()  # convierte en lista el contenido de una fila y lo m

        print(lista)
        print(str(lista[1]))
        print(type(lista[1]))
        db.commit()


        db.execute(
            'INSERT INTO cargaDiaria (centroSalud, fecha, respDisp, respOc, camaUTIDisp, camaUTIOc, camaGCDisp, camaGCOc, pacAlta, pacCOVIDAlta, pacFall, pacCOVIDFall, pacCOVIDUTI, pacUTI)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (int(lista[0]), str(lista[1]), str(lista[2]), lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9],
             lista[10], lista[11], lista[12], lista[13])  # TODO: placeholder
        )


@bp.route('/', methods=('GET', 'POST'))
@uploader_login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return url_for(upload.upload)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            storeData(file)
            flash('Succesfull upload')
            return redirect(url_for('upload.upload'))

    return render_template('uploader/uploadFile.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS