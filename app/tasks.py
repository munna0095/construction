from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app


def _now_local():
    return datetime.now(ZoneInfo(current_app.config['APP_TIMEZONE']))


def check_attendance_and_send_email(app):
    """Runs every minute from the scheduler. Sends the daily report once per day,
    at or after the configured reminder time."""
    with app.app_context():
        from app.models import Settings
        from app import db
        from app.notifications import send_attendance_report

        settings = Settings.query.first()
        if not settings or not settings.reminder_time:
            return

        now = _now_local()
        today = now.date()

        if settings.email_sent_date == today:
            return
        # 'HH:MM' strings compare correctly as text
        if now.strftime('%H:%M') < settings.reminder_time:
            return

        results = send_attendance_report(settings, today)
        # Mark as sent even if a channel failed, so failures do not repeat every minute.
        # Use the "Send report now" button on the settings page to retry.
        settings.email_sent_date = today
        db.session.commit()

        for channel, target, ok, error in results:
            status = 'sent' if ok else f'FAILED: {error}'
            print(f'[daily report] {channel} to {target}: {status}')
        if not results:
            print('[daily report] no email or Telegram recipients configured')
