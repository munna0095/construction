from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Labour, Project, Attendance
from sqlalchemy import func
from datetime import datetime, date, timedelta

bp = Blueprint('labour', __name__, url_prefix='/labour')

@bp.route('/')
@login_required
def index():
    query = request.args.get('q', '').strip()
    if query:
        labours = Labour.query.filter(Labour.name.ilike(f'%{query}%')).order_by(Labour.created_at.desc()).all()
    else:
        labours = Labour.query.order_by(Labour.created_at.desc()).all()
    # Calculate monthly cost for each labour (Total Present days in current month * daily_wage)
    today = date.today()
    first_day = date(today.year, today.month, 1)
    
    labour_data = []
    for l in labours:
        monthly_cost = db.session.query(func.sum(Attendance.daily_wage)).filter(
            Attendance.labour_id == l.id,
            Attendance.date >= first_day
        ).scalar() or 0.0
        
        # Check today's attendance
        today_attendance = Attendance.query.filter_by(labour_id=l.id, date=today).first()
        
        labour_data.append({
            'info': l,
            'monthly_cost': monthly_cost,
            'today_status': today_attendance.status if today_attendance else 'Not Marked'
        })
        
    return render_template('labour/index.html', labours=labour_data, title='Labour Management')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    projects = Project.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        daily_wage = request.form.get('daily_wage')
        fixed_salary = request.form.get('fixed_salary')
        address = request.form.get('address')
        project_id = request.form.get('project_id')
        
        if not phone or len(phone) != 10 or not phone.isdigit():
            flash('Invalid phone number. Please enter a valid 10-digit number.', 'danger')
            return render_template('labour/add.html', title='Add Labour', projects=projects)

        try:
            new_labour = Labour(
                name=name, 
                phone=phone, 
                daily_wage=float(daily_wage), 
                fixed_salary=float(fixed_salary) if fixed_salary else 0.0,
                address=address,
                project_id=int(project_id) if project_id else None
            )
            db.session.add(new_labour)
            db.session.commit()
            flash('Labour record added successfully!', 'success')
            return redirect(url_for('labour.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding record: {str(e)}', 'danger')
            
    return render_template('labour/add.html', title='Add Labour', projects=projects)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    labour = Labour.query.get_or_404(id)
    projects = Project.query.all()
    today = date.today()
    
    # Get month and year from args or default to today
    try:
        view_month = int(request.args.get('month', today.month))
        view_year = int(request.args.get('year', today.year))
    except:
        view_month = today.month
        view_year = today.year

    # Handle POST for Profile, Attendance entry, and Weekly Wages
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'save_attendance':
            att_date_str = request.form.get('att_date')
            att_status = request.form.get('att_status')
            if att_date_str and att_status:
                att_date = datetime.strptime(att_date_str, '%Y-%m-%d').date()
                
                # Check if it's in the future
                if att_date > today:
                    flash('Error: Cannot mark attendance for future dates.', 'danger')
                    return redirect(url_for('labour.edit', id=id, month=view_month, year=view_year))

                existing = Attendance.query.filter_by(labour_id=id, date=att_date).first()
                if existing:
                    existing.status = att_status
                    # If changed to absent, wage must be 0
                    if att_status == 'Absent':
                        existing.daily_wage = 0.0
                else:
                    wage = labour.daily_wage if att_status == 'Present' else 0.0
                    new_att = Attendance(labour_id=id, date=att_date, status=att_status, daily_wage=wage)
                    db.session.add(new_att)
                db.session.commit()
                flash(f'Attendance marked for {att_date_str}', 'success')
        
        elif action == 'update_weekly_wages':
            # Handle list of wages from the table
            for key, value in request.form.items():
                if key.startswith('wage_'):
                    date_str = key.replace('wage_', '')
                    try:
                        att_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        att = Attendance.query.filter_by(labour_id=id, date=att_date).first()
                        if att and att.status == 'Present':
                            att.daily_wage = float(value)
                    except: pass
            db.session.commit()
            flash('Weekly wages updated successfully!', 'success')

        else: # Update Profile
            phone = request.form.get('phone')
            if not phone or len(phone) != 10 or not phone.isdigit():
                flash('Invalid phone number.', 'danger')
            else:
                labour.name = request.form.get('name')
                labour.phone = phone
                labour.fixed_salary = float(request.form.get('fixed_salary') or 0.0)
                labour.address = request.form.get('address')
                pid = request.form.get('project_id')
                labour.project_id = int(pid) if pid else None
                try:
                    db.session.commit()
                    flash('Profile updated successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('labour.edit', id=id, month=view_month, year=view_year))

    # Calendar Logic
    import calendar
    cal = calendar.monthcalendar(view_year, view_month)
    month_dt = date(view_year, view_month, 1)
    month_name = month_dt.strftime('%B %Y')
    
    # Fetch all attendance for selected month
    month_start = date(view_year, view_month, 1)
    last_day = calendar.monthrange(view_year, view_month)[1]
    month_end = date(view_year, view_month, last_day)
    
    month_atts = Attendance.query.filter(
        Attendance.labour_id == id,
        Attendance.date >= month_start,
        Attendance.date <= month_end
    ).all()
    att_map = {a.date.day: a.status for a in month_atts}
    
    total_present = sum(1 for status in att_map.values() if status == 'Present')

    # Weekly Logic (Sunday to Saturday) - based on TODAY
    idx = (today.weekday() + 1) % 7 # 0 is Sunday
    sun_date = today - timedelta(days=idx)
    
    weekly_data = []
    total_weekly_wage = 0.0
    for i in range(7):
        current_day = sun_date + timedelta(days=i)
        att = Attendance.query.filter_by(labour_id=id, date=current_day).first()
        status_val = att.status if att else None
        
        wage = (att.daily_wage or 0.0) if att else 0.0
        total_weekly_wage += wage
        
        weekly_data.append({
            'sr': i + 1,
            'date': current_day.strftime('%Y-%m-%d'),
            'display_date': current_day.strftime('%d %b'),
            'day': current_day.strftime('%A'),
            'present': '✓' if status_val == 'Present' else '',
            'absent': '✗' if status_val == 'Absent' else '',
            'status': status_val,
            'wage': wage
        })
    
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    return render_template('labour/edit.html', 
                          labour=labour, 
                          projects=projects,
                          calendar=cal,
                          month_name=month_name,
                          view_month=view_month,
                          view_year=view_year,
                          months=months,
                          att_map=att_map,
                          total_present=total_present,
                          weekly_data=weekly_data,
                          total_weekly_wage=total_weekly_wage,
                          today=today,
                          title='Edit Labour')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    labour = Labour.query.get_or_404(id)
    try:
        # Also clean up attendance records
        Attendance.query.filter_by(labour_id=id).delete()
        db.session.delete(labour)
        db.session.commit()
        flash('Labour record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
    return redirect(url_for('labour.index'))
