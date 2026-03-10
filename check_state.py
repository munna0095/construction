from app import create_app, db
from app.models import User, Labour, Material, Project

app = create_app()

with app.app_context():
    print("--- Database State ---")
    users = User.query.all()
    print(f"Users: {len(users)}")
    for u in users:
        print(f" - {u.email} ({u.role})")
        
    projects = Project.query.all()
    print(f"Projects: {len(projects)}")
    for p in projects:
        print(f" - {p.name} [{p.status}]")
        
    labours = Labour.query.all()
    print(f"Labour Records: {len(labours)}")
    
    materials = Material.query.all()
    print(f"Material Records: {len(materials)}")
    print("----------------------")
