from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
scheduler = APScheduler()
login_manager.login_view = 'auth.login'

def _ensure_schema(app):
    """Create missing tables and add columns introduced after the DB was first created.
    Additive only: existing data is never dropped."""
    from sqlalchemy import inspect, text
    with app.app_context():
        db.create_all()
        columns = {c['name'] for c in inspect(db.engine).get_columns('settings')}
        if 'telegram_chat_ids' not in columns:
            db.session.execute(text('ALTER TABLE settings ADD COLUMN telegram_chat_ids VARCHAR(255)'))
            db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    _ensure_schema(app)

    # Initialize APScheduler
    scheduler.init_app(app)

    from app.tasks import check_attendance_and_send_email

    # Runs every minute; the task itself decides whether the daily report is due.
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
