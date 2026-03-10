from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Labour, Material, Project

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    labour_count = Labour.query.count()
    material_count = Material.query.count()
    project_count = Project.query.count()
    return render_template('dashboard.html', 
                           title='Dashboard',
                           labour_count=labour_count,
                           material_count=material_count,
                           project_count=project_count)
