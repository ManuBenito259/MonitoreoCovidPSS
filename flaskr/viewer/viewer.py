from flask import (
    Blueprint, render_template, request
)
from flaskr.auth import viewer_login_required
from flaskr.database.db import get_db
from datetime import datetime

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/estadisticas', methods=('GET', 'POST'))
@viewer_login_required
def estadisticas():
    db = get_db()
    ubicaciones = db.execute('SELECT * FROM cargaDiaria '
                             'JOIN centroSalud ON cargaDiaria.centroSalud = centroSalud.nombre '
                             'JOIN ubicacion ON centroSalud.ubicacion = ubicacion.cp').fetchall()

    if request.method == 'POST':
        jurisdiccion = request.form['Jurisdiccion']


        if(jurisdiccion == 'Todos'):
            posts = db.execute(
                'SELECT *'
                ' FROM cargaDiaria'
                ' ORDER BY id DESC'
            ).fetchall()
        else:
            posts = db.execute(
                'SELECT *'
                ' FROM cargaDiaria '
                'JOIN centroSalud ON cargaDiaria.centroSalud = centroSalud.nombre '
                'JOIN ubicacion ON centroSalud.ubicacion = ubicacion.cp'
                ' WHERE centroSalud.ubicacion = ?'
                ' ORDER BY id DESC'
                , (jurisdiccion,)
            ).fetchall()
        return render_template('viewer/Estadisticas.html', posts=posts, ubicaciones=ubicaciones)

    posts = db.execute(
        'SELECT *'
        ' FROM cargaDiaria'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('viewer/Estadisticas.html', posts=posts, ubicaciones=ubicaciones)










    return render_template('viewer/Estadisticas.html', posts=posts, ubicaciones=ubicaciones)


@bp.route('/')
@viewer_login_required
def index():
    return render_template('viewer/index.html')


@bp.route('/reportes')
@viewer_login_required
def reportes():
    db = get_db()

    reportes = db.execute(
        'SElECT SUM(pacNuevos) as pacNuevos, SUM(pacCovidNuevos) as pacCovidNuevos, ubicacion.provincia as provincia '\
        'FROM ' \
        'cargaDiaria JOIN centroSalud ON cargaDiaria.centroSalud = centroSalud.nombre '
        'JOIN ubicacion ON centroSalud.ubicacion = ubicacion.cp '\
        'GROUP BY fecha'
    ).fetchall()

    print(len(reportes))
    return render_template('viewer/Reportes.html', reportes=reportes)
