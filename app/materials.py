from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Material

bp = Blueprint('materials', __name__, url_prefix='/materials')

@bp.route('/')
@login_required
def index():
    materials = Material.query.order_by(Material.name).all()
    return render_template('materials/index.html', materials=materials, title='Materials Management')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        unit = request.form.get('unit')
        stock_quantity = request.form.get('stock_quantity')
        unit_price = request.form.get('unit_price')
        
        try:
            new_material = Material(
                name=name, 
                unit=unit, 
                stock_quantity=float(stock_quantity), 
                unit_price=float(unit_price)
            )
            db.session.add(new_material)
            db.session.commit()
            flash('Material record added successfully!', 'success')
            return redirect(url_for('materials.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding record: {str(e)}', 'danger')
            
    return render_template('materials/add.html', title='Add Material')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    material = Material.query.get_or_404(id)
    if request.method == 'POST':
        material.name = request.form.get('name')
        material.unit = request.form.get('unit')
        material.stock_quantity = float(request.form.get('stock_quantity'))
        material.unit_price = float(request.form.get('unit_price'))
        
        try:
            db.session.commit()
            flash('Material record updated successfully!', 'success')
            return redirect(url_for('materials.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating record: {str(e)}', 'danger')
            
    return render_template('materials/edit.html', material=material, title='Edit Material')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    material = Material.query.get_or_404(id)
    try:
        db.session.delete(material)
        db.session.commit()
        flash('Material record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
    return redirect(url_for('materials.index'))
