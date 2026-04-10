from flask import Flask
from .commands import create_admin

from src.app.extension import db, login_manager
from src.config.settings import configClass

def create_app():
    app = Flask(__name__)
    app.config.from_object(configClass)

    #Inicializar extensiones
    db.init_app(app)
    app.cli.add_command(create_admin)
    login_manager.init_app(app)
    setattr(login_manager, 'login_view', 'auth.login')
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "info"

    with app.app_context():
        import src.app.models.model

        if app.config.get('AUTO_CREATE_TABLES'):
            db.create_all()

    from src.app.routes.routes_public import bp as bp_public
    app.register_blueprint(bp_public)

    from src.app.routes.routes_admin import bp as bp_admin
    app.register_blueprint(bp_admin)

    from src.app.routes.auth_routes import bp as bp_auth
    app.register_blueprint(bp_auth)

    return app