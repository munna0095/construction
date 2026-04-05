from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
scheduler = APScheduler()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Initialize APScheduler
    scheduler.init_app(app)
    
    from app.tasks import check_attendance_and_send_email
    
    @scheduler.task('cron', id='attendance_reminder', minute='*')
    def run_reminder():
        check_attendance_and_send_email(app)
        
    scheduler.start()

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
