from datetime import date, datetime
import smtplib
from email.message import EmailMessage

def check_attendance_and_send_email(app):
    with app.app_context():
        from app.models import Settings, Attendance, Labour
        from app import db
        
        settings = Settings.query.first()
        if not settings or not settings.admin_email:
            return
            
        now = datetime.now()
        current_time_str = now.strftime('%H:%M')
        
        # Check if it's the exact minute to send the reminder
        if settings.reminder_time == current_time_str:
            today = date.today()
            
            # Check if we already sent an email today
            if settings.email_sent_date == today:
                return
                
            total_labours = Labour.query.count()
            attendance_count = Attendance.query.filter_by(date=today).count()
            
            # If any attendance is missing
            if attendance_count < total_labours:
                missing = total_labours - attendance_count
                
                # We will just print the notification for now instead of failing on SMTP connection
                # The user can configure real SMTP credentials locally if needed
                print(f"\n====================== SYSTEM NOTIFICATION ======================")
                print(f"TO: {settings.admin_email}")
                print(f"SUBJECT: MISSING ATTENDANCE REMINDER")
                print(f"BODY: You have {missing} labourer(s) missing attendance for {today.strftime('%d %b %Y')}.")
                print(f"Please log in to http://127.0.0.1:5000/labour/bulk_attendance to update.")
                print(f"=================================================================\n")
                
                settings.email_sent_date = today
                db.session.commit()
