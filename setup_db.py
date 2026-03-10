from app import create_app, db
from app.models import User, Project, Material, Labour

app = create_app()

with app.app_context():
    db.drop_all() # Reset for schema changes
    db.create_all()
    
    # Check if test user exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(name='Admin User', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Add a sample project
        sample_project = Project(
            name='Luxury Heights - Phase 1',
            location='Downtown Metropolitan',
            status='In Progress',
            description='15-story residential complex with premium amenities.'
        )
        db.session.add(sample_project)
        db.session.flush() # Get project id

        # Add sample labour linked to project
        sample_labour = Labour(
            name='Rajesh Kumar',
            phone='9876543210',
            address='123, Green Street, City Center',
            daily_wage=800.0,
            fixed_salary=15000.0,
            project_id=sample_project.id
        )
        db.session.add(sample_labour)
        
        db.session.commit()
        print("Database initialized with Admin User, Sample Project, and Labour.")
    else:
        print("Database already initialized.")
