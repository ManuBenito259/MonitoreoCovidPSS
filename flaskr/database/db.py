import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def create_admin(db):
    db.execute('INSERT INTO users (username, password, type) VALUES (?,?,?)',
               ("admin", generate_password_hash("admin"), "admin"))
    db.commit()

def init_db():
    db = get_db()

    with current_app.open_resource('database\schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        create_admin(db)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
