from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Settings
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_obj = Settings.query.first()
    if not settings_obj:
        settings_obj = Settings(admin_email='', reminder_time='19:00')
        db.session.add(settings_obj)
        db.session.commit()

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'auth':
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if new_password and new_password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('auth.settings'))

            if User.query.filter(User.email == new_email, User.id != current_user.id).first():
                flash('Email already in use', 'danger')
                return redirect(url_for('auth.settings'))

            current_user.email = new_email
            if new_password:
                current_user.set_password(new_password)
            
            db.session.commit()
            flash('Admin credentials updated successfully', 'success')
            
        elif action == 'email_reminder':
            settings_obj.admin_email = request.form.get('admin_email')
            settings_obj.reminder_time = request.form.get('reminder_time')
            db.session.commit()
            flash('Email reminder settings updated successfully', 'success')
            
        return redirect(url_for('auth.settings'))

    return render_template('auth/settings.html', title='Admin Settings', app_settings=settings_obj)

def send_reset_email(user):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # We will use dummy configuration variables that the user must replace
    sender_email = "your_email@gmail.com"  # The sender email
    sender_password = "your_app_password"  # The sender App Password
    
    token = user.get_reset_token()
    # Assuming standard route setup
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = sender_email
    msg["To"] = user.email
    
    text = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    msg.attach(MIMEText(text))
    
    try:
        # If credentials are not set, immediately skip the hanging SMTP connection
        if sender_password == "your_app_password":
            print("\n" + "="*50)
            print("RESET URL (Email Not Configured!):")
            print(reset_url)
            print("="*50 + "\n")
            return
            
        # We try to connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user.email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Failed to send email:", e)
        # Fallback: Print URL to console for development so user isn't locked out immediately
        print("\n" + "="*50)
        print("RESET URL (Use this if email fails):")
        print(reset_url)
        print("="*50 + "\n")
        return False

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            send_reset_email(user)
        # We flash success even if email doesn't exist to prevent email discovery
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        user.set_password(password)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password')
