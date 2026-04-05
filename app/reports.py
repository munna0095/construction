from flask import Blueprint, render_template, request, send_file, redirect, url_for
from flask_login import login_required
from app.models import Labour, Material, Attendance
from app import db
from sqlalchemy import func
from datetime import date, timedelta, datetime

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    # Handle Date Range Cycles
    today = date.today()
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    preset = request.args.get('preset')
    
    # Default: Current Week (Sunday-Friday, 6 days)
    idx = (today.weekday() + 1) % 7 # 0 is Sunday
    week_start = today - timedelta(days=idx)
    week_end = week_start + timedelta(days=5) # Friday
    
    if preset == 'last_week':
        week_start = week_start - timedelta(days=7)
        week_end = week_start + timedelta(days=5)
    elif start_str and end_str:
        try:
            week_start = datetime.strptime(start_str, '%Y-%m-%d').date()
            week_end = datetime.strptime(end_str, '%Y-%m-%d').date()
            
            # Check for 6-day limit
            if (week_end - week_start).days > 5:
                from flask import flash
                flash('Select upto 6 days only', 'danger')
                # Redirect with original start_date to let user try again
                return redirect(url_for('reports.index', start_date=start_str))
        except ValueError:
            pass # Use defaults if invalid

    # Basic statistics
    labour_count = Labour.query.count()
    material_count = Material.query.count()
    
    # Financial summary (All time for overview stats, but filterable if needed)
    total_material_value = 0
    materials = Material.query.all()
    for m in materials:
        total_material_value += (m.stock_quantity * m.unit_price)
        
    avg_daily_wage = db.session.query(func.avg(Labour.daily_wage)).scalar() or 0
    
    # Weekly Report Data (Now using the defined cycle)
    labours = Labour.query.all()
    weekly_report = []
    
    # Number of days in current cycle for the table
    delta = (week_end - week_start).days + 1
    cycle_days = []
    for d in range(min(delta, 6)): # Limit display to 6 days for width and policy (Sunday-Friday)
        cycle_days.append(week_start + timedelta(days=d))
    
    grand_total_advance = 0.0
    grand_total_payable = 0.0

    for i, l in enumerate(labours):
        row = {
            'sr': i + 1,
            'name': l.name,
            'days': [],
            'total_days_present': 0,
            'payable_amount': 0.0,
            'total_advance': 0.0,
            'id': l.id
        }
        
        # Sum the wages stored in each attendance record for the cycle
        cycle_attendance = Attendance.query.filter(
            Attendance.labour_id == l.id,
            Attendance.date >= week_start,
            Attendance.date <= week_end
        ).all()
        att_day_map = {a.date: a for a in cycle_attendance}
        
        for cd in cycle_days:
            att = att_day_map.get(cd)
            status = 'P' if att and att.status == 'Present' else ('A' if att and att.status == 'Absent' else '-')
            row['days'].append(status)
            if status == 'P':
                row['total_days_present'] += 1
            if att:
                row['payable_amount'] += (att.daily_wage or 0.0)
                row['total_advance'] += (att.advance or 0.0)
        
        grand_total_advance += row['total_advance']
        grand_total_payable += row['payable_amount']
        weekly_report.append(row)

    return render_template('reports/index.html', 
                            title='Reports & Analytics',
                            labour_count=labour_count,
                            material_count=material_count,
                            total_material_value=total_material_value,
                            avg_daily_wage=avg_daily_wage,
                            weekly_report=weekly_report,
                            cycle_days=cycle_days,
                            grand_total_advance=grand_total_advance,
                            grand_total_payable=grand_total_payable,
                            week_start=week_start,
                            week_end=week_end,
                            preset=preset,
                            week_range=f"{week_start.strftime('%d %b')} - {week_end.strftime('%d %b %Y')}")

@bp.route('/download')
@login_required
def download_report():
    # Pass parameters to the print preview
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Similar logic to index to fetch data for the print view
    # For reliability, we redirect to a specific 'printable' route 
    # that has a cleaner CSS for 'Save to PDF'
    return redirect(url_for('reports.print_view', start_date=start_date, end_date=end_date))

@bp.route('/print')
@login_required
def print_view():
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    
    # Default Cycle logic
    today = date.today()
    idx = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=idx)
    week_end = week_start + timedelta(days=5) # Friday
    
    if start_str and end_str:
        try:
            week_start = datetime.strptime(start_str, '%Y-%m-%d').date()
            week_end = datetime.strptime(end_str, '%Y-%m-%d').date()
            # Also limit print view to 6 days
            if (week_end - week_start).days > 5:
                week_end = week_start + timedelta(days=5)
        except: pass

    labours = Labour.query.all()
    weekly_report = []
    delta = (week_end - week_start).days + 1
    cycle_days = [week_start + timedelta(days=d) for d in range(min(delta, 6))] 
    
    grand_total_advance = 0.0
    grand_total_payable = 0.0

    for i, l in enumerate(labours):
        # Sum the wages stored in each attendance record for the cycle
        cycle_attendance = Attendance.query.filter(
            Attendance.labour_id == l.id,
            Attendance.date >= week_start,
            Attendance.date <= week_end
        ).all()
        att_day_map = {a.date: a for a in cycle_attendance}
        
        row_days = []
        total_days_present = 0
        cycle_payable = 0.0
        cycle_advance = 0.0
        for cd in cycle_days:
            att = att_day_map.get(cd)
            status = 'P' if att and att.status == 'Present' else ('A' if att and att.status == 'Absent' else '-')
            row_days.append(status)
            if status == 'P':
                total_days_present += 1
            if att:
                cycle_payable += (att.daily_wage or 0.0)
                cycle_advance += (att.advance or 0.0)

        row = {
            'sr': i + 1,
            'name': l.name,
            'days': row_days,
            'total_days_present': total_days_present,
            'payable_amount': cycle_payable,
            'total_advance': cycle_advance
        }
        grand_total_advance += cycle_advance
        grand_total_payable += cycle_payable
        weekly_report.append(row)

    return render_template('reports/print.html', 
                          weekly_report=weekly_report,
                          cycle_days=cycle_days,
                          grand_total_advance=grand_total_advance,
                          grand_total_payable=grand_total_payable,
                          week_range=f"{week_start.strftime('%d %b')} - {week_end.strftime('%d %b %Y')}",
                          today=datetime.now())
