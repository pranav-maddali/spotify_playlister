from flask import Flask

from app.extensions import login_manager, db
from app.commands import create_tables
from app.models import User
from app.routes import main

def create_app(config_file='config.py'):
    application = Flask(__name__)

    application.config.from_pyfile(config_file)

    db.init_app(application)

    login_manager.init_app(application)

    from app import routes
    login_manager.login_view = 'routes.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    application.register_blueprint(main)

    application.cli.add_command(create_tables)

    return application
