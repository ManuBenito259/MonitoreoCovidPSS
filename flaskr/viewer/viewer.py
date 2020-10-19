from flask import (
    Blueprint,render_template
)
from flaskr.auth import viewer_login_required
from flaskr.database.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/')
@viewer_login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT *'
        ' FROM cargaDiaria'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('viewer/index.html', posts=posts)
