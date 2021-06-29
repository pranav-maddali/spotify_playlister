from flask.cli import with_appcontext

from app.extensions import db
from app.models import User

@with_appcontext
def create_tables():
    db.create_all()
