"""Daily attendance report: builds the message and sends it by email and Telegram.

Uses only the standard library for HTTP/SMTP, so no new dependencies are needed.
"""
import json
import re
import smtplib
import urllib.parse
import urllib.request
from email.message import EmailMessage

from flask import current_app

from app.models import Attendance, Labour


def normalize_chat_id(value):
    """Telegram chat IDs are integers (negative for groups). Return the cleaned ID or None."""
    value = (value or '').strip()
    if re.fullmatch(r'-?\d{5,20}', value):
        return value
    return None


def parse_chat_ids(raw):
    """Split the stored comma-separated value into a list of chat IDs."""
    return [c for c in (normalize_chat_id(p) for p in (raw or '').split(',')) if c]


def build_report(today):
    """Collect today's attendance and format the message.

    'missing' means at least one labour has no attendance row for today.
    """
    labours = Labour.query.order_by(Labour.name).all()
    status_by_labour = {
        a.labour_id: a.status
        for a in Attendance.query.filter_by(date=today).all()
    }

    present, absent, unmarked = [], [], []
    for labour in labours:
        status = status_by_labour.get(labour.id)
        if status == 'Present':
            present.append(labour.name)
        elif status == 'Absent':
            absent.append(labour.name)
        else:
            unmarked.append(labour.name)

    missing = len(unmarked) > 0
    date_label = today.strftime('%d %b %Y')
    link = current_app.config['APP_BASE_URL'].rstrip('/') + '/labour/bulk_attendance'

    def names(lst):
        return ', '.join(lst) if lst else 'None'

    if not labours:
        headline = 'No labour records found.'
    elif missing:
        headline = f'Attendance NOT logged yet for {date_label}. {len(unmarked)} labour(s) not marked.'
    else:
        headline = f'Attendance logged for {date_label}.'

    lines = [
        'SIDDHI CONSTRUCTION - Daily attendance',
        '',
        headline,
        '',
        f'Total labour: {len(labours)}',
        f'Present ({len(present)}): {names(present)}',
        f'Absent ({len(absent)}): {names(absent)}',
    ]
    if missing:
        lines.append(f'Not marked ({len(unmarked)}): {names(unmarked)}')
        lines += ['', f'Please log attendance here: {link}']

    subject = (f'ATTENDANCE NOT LOGGED - {date_label}' if missing
               else f'Attendance summary - {date_label}')

    return {
        'missing': missing,
        'subject': subject,
        'body': '\n'.join(lines),
        'present': present,
        'absent': absent,
        'unmarked': unmarked,
    }


def send_email(to_address, subject, body):
    cfg = current_app.config
    if not cfg['SMTP_USER'] or not cfg['SMTP_PASSWORD']:
        raise RuntimeError('SMTP_USER / SMTP_PASSWORD are not set on the server')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = cfg['SMTP_USER']
    msg['To'] = to_address
    msg.set_content(body)

    with smtplib.SMTP(cfg['SMTP_HOST'], cfg['SMTP_PORT'], timeout=20) as server:
        server.starttls()
        server.login(cfg['SMTP_USER'], cfg['SMTP_PASSWORD'])
        server.send_message(msg)


def send_telegram(chat_id, text):
    token = current_app.config['TELEGRAM_BOT_TOKEN']
    if not token:
        raise RuntimeError('TELEGRAM_BOT_TOKEN is not set on the server')

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=20) as response:
        result = json.loads(response.read())
    if not result.get('ok'):
        raise RuntimeError(result.get('description', 'Telegram rejected the message'))
    return result


def send_attendance_report(settings, today):
    """Build today's report and send it to the admin email and all Telegram chats.

    Returns a list of (channel, target, ok, error) tuples, one per attempted send.
    Each channel is attempted independently, so one failure does not block the rest.
    """
    report = build_report(today)
    results = []

    if settings.admin_email:
        try:
            send_email(settings.admin_email, report['subject'], report['body'])
            results.append(('email', settings.admin_email, True, ''))
        except Exception as exc:
            current_app.logger.exception('Email report failed')
            results.append(('email', settings.admin_email, False, str(exc)))

    text = report['subject'] + '\n\n' + report['body']
    for chat_id in parse_chat_ids(settings.telegram_chat_ids):
        try:
            send_telegram(chat_id, text)
            results.append(('telegram', chat_id, True, ''))
        except Exception as exc:
            current_app.logger.exception('Telegram report failed for %s', chat_id)
            results.append(('telegram', chat_id, False, str(exc)))

    return results
