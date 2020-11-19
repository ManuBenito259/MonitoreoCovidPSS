from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import viewer_login_required, uploader_login_required
from flaskr.database.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if g.user:
        if g.user['type'] == "viewer":
            return redirect(url_for('data.index'))

        if g.user['type'] == "uploader":
            return redirect(url_for('upload.index'))

        if g.user['type'] == "admin":
            return redirect(url_for('admin.admin_index'))
    return render_template('home/home.html')
