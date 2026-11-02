import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Timezone used to decide when the daily report is due (server clock may be UTC)
    APP_TIMEZONE = os.environ.get('APP_TIMEZONE') or 'Asia/Kolkata'
    # Link included in notifications so the admin can open the attendance page
    APP_BASE_URL = os.environ.get('APP_BASE_URL') or 'http://168.144.30.73:5000'

    # Email (SMTP). For Gmail use an App Password, not your normal password.
    SMTP_HOST = os.environ.get('SMTP_HOST') or 'smtp.gmail.com'
    SMTP_PORT = int(os.environ.get('SMTP_PORT') or 587)
    SMTP_USER = os.environ.get('SMTP_USER') or ''
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or ''

    # Telegram bot token from @BotFather
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or ''
