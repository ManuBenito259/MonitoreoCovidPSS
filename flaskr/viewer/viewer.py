from flask import (
    Blueprint, render_template
)
from flaskr.auth import viewer_login_required
from flaskr.database.db import get_db
from datetime import datetime

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/estadisticas')
@viewer_login_required
def estadisticas():
    pacientesCovid = 0
    pacientesCovidAlta = 0
    pacientesCovidFallecidos = 0
    db = get_db()
    posts = db.execute(
        'SELECT *'
        ' FROM cargaDiaria'
        ' ORDER BY id DESC'
    ).fetchall()

    return render_template('viewer/Estadisticas.html', posts=posts)


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

   #SUM(pacNuevos) as pacNuevos, SUM(pacCovidNuevos) as pacVovidNuevos, '
#    'SUM(pacFall) as pacFall, ubicacion.provincia as provincia

# JOIN centroSalud ON cargaDiaria.centroSalud = centroSalud.id ' \
#         'JOIN ubicacion ON centroSalud.ubicacion = ubicacion.cp
   #
   #dat = datetime.utcnow().strftime('%d/%m/%Y')  # Obtiene la fecha de un dia desps, no se xq

   #s = 'SELECT * FROM cargaDiaria WHERE fecha like "' + dat + '"'
   #print(s)
   #posts2 = db.execute(
   #    s
   #).fetchall()

   #for posteos in posts2:
   #    pacientesCovid = pacientesCovid + posteos['pacNuevos']
   #    pacientesCovidAlta = pacientesCovidAlta + posteos['pacCOVIDAlta']
   #    pacientesCovidFallecidos = pacientesCovidFallecidos + posteos['pacCOVIDFall']
