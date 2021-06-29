from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import config

application = Flask(__name__)

application.config['SECRET_KEY'] = db_secret_key
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

db = SQLAlchemy(application)

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.init_app(application)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes

if __name__ == "__main__":
    application.run(debug=True)
