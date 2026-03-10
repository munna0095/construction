from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Project, Material, Labour, Attendance, Transaction
from app import db
from sqlalchemy import func
from datetime import datetime, date

bp = Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/')
@login_required
def index():
    projects = Project.query.all()
    project_data = []
    for p in projects:
        # Calculate material/expense cost only (Labour cost removed per request)
        total_expense = db.session.query(func.sum(Transaction.total_cost)).filter(
            Transaction.project_id == p.id
        ).scalar() or 0.0
        
        project_data.append({
            'info': p,
            'total_cost': total_expense,
            'labour_count': len(p.labours)
        })
        
    return render_template('projects/index.html', projects=project_data, title='Project Portfolio')

@bp.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST' and 'exp_name' in request.form:
        exp_name = request.form.get('exp_name')
        qty = request.form.get('quantity')
        cost = request.form.get('cost')
        payment_status = request.form.get('payment_status')
        notes = request.form.get('notes')
        
        try:
            # Handle as general expense if quantity is not provided or it's a non-material item
            # We can still link to Material if name matches, but quantity is now optional.
            material = Material.query.filter_by(name=exp_name, project_id=project.id).first()
            
            transaction = Transaction(
                project_id=project.id,
                material_id=material.id if material else None,
                type='EXPENSE',
                quantity=float(qty) if qty and qty.strip() else None,
                total_cost=float(cost),
                payment_status=payment_status,
                notes=notes if notes else f"Expense: {exp_name}"
            )
            
            if material and qty and qty.strip():
                material.stock_quantity += float(qty)
            
            db.session.add(transaction)
            db.session.commit()
            flash('Expense/Material record added successfully!', 'success')
            return redirect(url_for('projects.view', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding record: {str(e)}', 'danger')

    # Data for view
    transactions = Transaction.query.filter_by(project_id=id).order_by(Transaction.date.desc()).all()
    total_project_cost = sum(t.total_cost for t in transactions)
    
    # We still show labour list but without costs added to total
    project_labours = Labour.query.filter_by(project_id=id).all()
    labour_data = []
    for l in project_labours:
        present_count = Attendance.query.filter_by(labour_id=l.id, status='Present').count()
        absent_count = Attendance.query.filter_by(labour_id=l.id, status='Absent').count()
        labour_data.append({
            'name': l.name,
            'present': present_count,
            'absent': absent_count
        })

    return render_template('projects/view.html', 
                          project=project, 
                          expenses=transactions,
                          total_project_cost=total_project_cost,
                          labour_data=labour_data,
                          title=f'SIDDHI - {project.name}')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        status = request.form.get('status')
        description = request.form.get('description')
        
        try:
            new_project = Project(
                name=name,
                location=location,
                status=status,
                description=description
            )
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('projects.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {str(e)}', 'danger')
            
    return render_template('projects/add.html', title='Add Project')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.location = request.form.get('location')
        project.status = request.form.get('status')
        project.description = request.form.get('description')
        
        try:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('projects.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'danger')
            
    return render_template('projects/edit.html', project=project, title='Edit Project')

@bp.route('/edit_expense/<int:id>', methods=['POST'])
@login_required
def edit_expense(id):
    transaction = Transaction.query.get_or_404(id)
        
    exp_name = request.form.get('exp_name')
    qty = request.form.get('quantity')
    cost = request.form.get('cost')
    payment_status = request.form.get('payment_status')
    notes = request.form.get('notes')
    
    try:
        # If it was linked to a material, we might need to adjust stock if quantity changed
        if transaction.material_id:
            material = Material.query.get(transaction.material_id)
            old_qty = transaction.quantity or 0.0
            new_qty = float(qty) if qty and qty.strip() else 0.0
            material.stock_quantity += (new_qty - old_qty)
            transaction.quantity = new_qty
        elif qty and qty.strip():
            transaction.quantity = float(qty)
        else:
            transaction.quantity = None

        transaction.total_cost = float(cost)
        transaction.payment_status = payment_status
        # Handle notes to preserve "Expense: " prefix if wanted, or just use what's provided
        if exp_name:
            transaction.notes = f"Expense: {exp_name}"
            if notes:
                transaction.notes += f" - {notes}"
        else:
            transaction.notes = notes
            
        db.session.commit()
        flash('Expense record updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating record: {str(e)}', 'danger')
        
    return redirect(url_for('projects.view', id=transaction.project_id))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    project = Project.query.get_or_404(id)
    try:
        # Also clean up linked data or nullify? User wants project panel to contain materials.
        # If project deleted, maybe materials should be deleted too.
        Material.query.filter_by(project_id=id).delete()
        Transaction.query.filter_by(project_id=id).delete()
        # Labour records should be unlinked
        for l in project.labours:
            l.project_id = None
            
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {str(e)}', 'danger')
    return redirect(url_for('projects.index'))

@bp.route('/delete_expense/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    transaction = Transaction.query.get_or_404(id)
    project_id = transaction.project_id
    try:
        # If it was linked to a material, we might want to adjust stock?
        # For now, just delete the transaction as requested.
        if transaction.material_id and transaction.quantity:
            material = Material.query.get(transaction.material_id)
            material.stock_quantity -= transaction.quantity
            
        db.session.delete(transaction)
        db.session.commit()
        flash('Expense record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
    return redirect(url_for('projects.view', id=project_id))
