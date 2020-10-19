from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import viewer_login_required, uploader_login_required
from flaskr.database.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('home/home.html')

