import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)

from flaskr.auth import uploader_login_required
from flaskr.database.db import get_db

bp = Blueprint('upload', __name__, url_prefix='/upload')
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}
DEFAULT_NAME = "PlanillaExterna.xlsx"


def storeData(file):
    df = pd.read_excel(file, 'Sheet1')
    db = get_db()
    rows = df.shape[0]  # obtiene el numero de filas (sin contar el encabezado)
        
    lista = df.loc[0].tolist()  # convierte en lista el contenido de una fila
    
    db.execute(
        'INSERT INTO cargaDiaria (centroSalud, fecha, respDisp, respOc, camaUTIDisp, camaUTIOc, camaGCDisp, camaGCOc, pacNuevos, pacCovidNuevos, pacAlta, pacCOVIDAlta, pacFall, pacCOVIDFall, pacCOVIDUTI, pacUTI)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (str(lista[0]), str(lista[1]), str(lista[2]), str(lista[3]), str(lista[4]), str(lista[5]), str(lista[6]),
        str(lista[7]), 0,0,0,0,0,0,0,0)  # TODO: placeholder
    )
    idCarga = db.execute('SELECT last_insert_id(cargaDiaria)')
    db.commit()
    return idCarga


@bp.route('/datosHospital', methods=('GET', 'POST'))
@uploader_login_required
def uploadDatosHospital():
    if request.method == 'POST' and request.form['submitButton'] == 'Subir Archivo':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return url_for(uploadDatosHospital.upload)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            idCarga = storeData(file)
            flash('Succesfull upload')
            return redirect(url_for('upload.uploadPacientes', id = idCarga))
    if request.method == 'POST' and request.form['submitButton'] == 'SaveCarga':
        centroSalud = request.form[
            'centroSalud']  # TODO: El centro de salud deberia obtenerse a partir de el usuario logueado para evitar inconsistencias
        fecha = request.form['fecha']
        respiradoresDisp = request.form['respiradoresDisponibles']
        respiradoresOc = request.form['respiradoresOcupados']
        camaUTIDisp = request.form['camasUTIDisponibles']
        camaUTIOc = request.form['camasUTIOcupadas']
        camaGCDisp = request.form['camasGCDisponibles']
        camaGCOc = request.form['camasGCOcupadas']

        db = get_db()

        error = None

        fechaDB = db.execute(
            'SELECT DISTINCT fecha FROM cargaDiaria WHERE centroSalud = ? AND fecha = ?', (centroSalud, fecha,)
        ).fetchone()

        if fechaDB is not None:
            error = 'El centro de salud ' + centroSalud + ' ya realizó una carga el día de hoy'

        if (int(respiradoresDisp) < 0) or (int(respiradoresOc) < 0) or (int(camaUTIDisp) < 0) or (
                int(camaUTIOc) < 0) or (int(camaGCDisp) < 0) or (int(camaGCOc) < 0):
            error = 'ERROR: No es posible cargar valores negativos'

        if error is None:
            session['carga'] = {}
            session['carga']['centro'] = centroSalud
            session['carga']['camaGCDisp'] = camaGCDisp
            session['carga']['camaGCOc'] = camaGCOc
            session['carga']['camaUTIOc'] = camaUTIOc
            session['carga']['camaUTIDisp'] = camaUTIDisp
            session['carga']['respiradoresDisp'] = respiradoresDisp
            session['carga']['respiradoresOc'] = respiradoresOc
            session['carga']['fecha'] = fecha
            session['carga']['centroSalud'] = centroSalud
            session['carga']['pacNuevos'] = 0
            session['carga']['pacCovidNuevos'] = 0
            session['carga']['pacFall'] = 0
            session['carga']['pacCovidFall'] = 0
            session['carga']['pacAlta'] = 0
            session['carga']['pacCovidAlta'] = 0
            session['carga']['pacCovidUTI'] = 0
            session['carga']['pacUTI'] = 0


            return redirect(url_for('upload.uploadPacientes', id = 0))
        else:
            flash(error)
    # TODO: los campos deberían volver a estar vacíos

    db = get_db()
    centros = db.execute(
        'SELECT *'
        ' FROM centroSalud'
    ).fetchall()
    return render_template('uploader/uploadDatosHospital.html', centros=centros)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def storePacientes(file,id):
    df = pd.read_excel(file, 'Sheet1')
    db = get_db()
    rows = df.shape[0]  # obtiene el numero de filas (sin contar el encabezado)
        
    lista = df.loc[0].tolist()  # convierte en lista el contenido de una fila
    
    db.execute(
        'UPDATE cargaDiaria SET pacNuevos = ?, pacCovidNuevos = ?, pacAlta = ?, pacCOVIDAlta = ?, pacFall = ?, pacCOVIDFall = ?, pacCOVIDUTI = ?, pacUTI = ?'
        'WHERE id = ?',
        (str(lista[0]), str(lista[1]), str(lista[2]), str(lista[3]), str(lista[4]),
        str(lista[5]), str(lista[6]), str(lista[7]), id)  # TODO: placeholder
    )
    db.commit()

@bp.route('/<string:id>/datosPacientes', methods=('GET', 'POST'))
@uploader_login_required
def uploadPacientes(id):

    if request.method == 'POST' and request.form['submitButton'] == 'SubirArchivo':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return url_for(uploadDatosHospital.upload)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            storePacientes(file,id)
            flash('Succesfull upload')
            return redirect(url_for('upload.uploadPacientes', id = id))

    elif request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        estado = request.form['estado']
        print(estado)

        db = get_db()
        db.execute(
            'INSERT INTO paciente (dni, nombre, apellido, telefono, estado)'
            ' VALUES (?, ?, ?, ?, ?)',
            (dni, nombre, apellido, telefono, estado,)
        )

        if estado == 'InternadoCovid':
            print("conto un paciente comun")
            print(session['carga']['pacNuevos'])
            session['carga']['pacNuevos'] = int(session['carga']['pacNuevos']) +1
            print(session['carga']['pacNuevos'])
        else: #if estado == 'InternadoClinico':
            print("conto un paciente covid")
            print(session['carga']['pacCovidNuevos'])
            session['carga']['pacCovidNuevos'] = (1 + int(session['carga']['pacCovidNuevos']))

        if request.form['submitButton'] == 'CargarPaciente':
            return redirect(url_for('upload.uploadPacientes', id = 0))

        if request.form['submitButton'] == 'Finalizar':
            return redirect(url_for('upload.uploadEstadoPacientes'))

    return render_template('uploader/uploadPacientes.html', id=id)


@bp.route('/estadoPacientes', methods=('GET', 'POST'))
@uploader_login_required
def uploadEstadoPacientes():
    if request.method == 'POST' and request.form['submitButton'] == 'Finalizar':
        centro = session['carga']['centro']
        fecha = session['carga']['fecha']
        respDisp = session['carga']['respiradoresDisp']
        respOc = session['carga']['respiradoresOc']
        camaUTIDisp = session['carga']['camaUTIDisp']
        camaUTIOc = session['carga']['camaUTIOc']
        camaGCDisp = session['carga']['camaGCDisp']
        camaGCOc = session['carga']['camaGCOc']
        pacNuevos = session['carga']['pacNuevos']
        pacCovidNuevos = session['carga']['pacCovidNuevos']
        pacAlta = session['carga']['pacAlta']
        pacCovidAlta = session['carga']['pacCovidAlta']
        pacFall = session['carga']['pacFall']
        pacCovidFall = session['carga']['pacCovidFall']
        pacCovidUTI = session['carga']['pacCovidUTI']
        pacUTI = session['carga']['pacUTI']


        db = get_db()
        db.execute(
            'INSERT INTO cargaDiaria (centroSalud, fecha, respDisp, respOc, camaUTIDisp, camaUTIOc, camaGCDisp, camaGCOc, pacCovidNuevos, pacNuevos, pacAlta, pacCOVIDAlta, pacFall, pacCOVIDFall, pacCOVIDUTI, pacUTI)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (centro, fecha, respDisp, respOc, camaUTIDisp, camaUTIOc, camaGCDisp, camaGCOc, pacNuevos, pacCovidNuevos, pacAlta, pacCovidAlta, pacFall, pacCovidFall, pacCovidUTI, pacUTI)
        )
        db.commit()
        return(redirect(url_for('upload.uploadDatosHospital')))



    db = get_db()
    pacientes = db.execute(
        'SELECT *'
        ' FROM paciente'
    ).fetchall()
    return render_template('uploader/uploadEstadoPaciente.html', pacientes=pacientes)
