from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
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
    if request.method == 'POST':
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
        flash('Settings updated successfully', 'success')
        return redirect(url_for('auth.settings'))

    return render_template('auth/settings.html', title='Admin Settings')
