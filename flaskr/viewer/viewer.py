from flask import (
    Blueprint,render_template
)
from flaskr.auth import viewer_login_required
from flaskr.database.db import get_db
from datetime import datetime

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/')
@viewer_login_required
def index():
    pacientesCovid = 0
    pacientesCovidAlta = 0
    pacientesCovidFallecidos = 0
    db = get_db()
    posts = db.execute(
        'SELECT *'
        ' FROM cargaDiaria'
        ' ORDER BY id DESC'
    ).fetchall()

    dat=datetime.utcnow().strftime('%d/%m/%Y') #Obtiene la fecha de un dia desps, no se xq

    s='SELECT * FROM cargaDiaria WHERE fecha like "' + dat + '"'
    print(s)
    posts2 = db.execute(
        s
    ).fetchall()


    for posteos in posts2:
        pacientesCovid= pacientesCovid + posteos['pacNuevos']
        pacientesCovidAlta=pacientesCovidAlta + posteos['pacCOVIDAlta']
        pacientesCovidFallecidos=pacientesCovidFallecidos + posteos['pacCOVIDFall']
    return render_template('viewer/index.html', posts=posts, pacientesCovid=pacientesCovid,pacientesCovidAlta=pacientesCovidAlta,pacientesCovidFallecidos=pacientesCovidFallecidos)
