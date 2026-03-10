from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Placeholders for other components
    from app.labour import bp as labour_bp
    app.register_blueprint(labour_bp)

    from app.materials import bp as materials_bp
    app.register_blueprint(materials_bp)

    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp)

    from app.projects import bp as projects_bp
    app.register_blueprint(projects_bp)

    return app
