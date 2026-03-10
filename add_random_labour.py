import random
from app import create_app, db
from app.models import Labour, Project

app = create_app()

names = [
    "Aarav Sharma", "Vivaan Gupta", "Aditya Singh", "Vihaan Patel", 
    "Arjun Verma", "Sai Reddy", "Ishaan Kapoor", "Shaurya Joshi", 
    "Aryan Malhotra", "Kabir Bhat"
]

addresses = [
    "123, MG Road, Bengaluru", "45, Park Street, Kolkata",
    "67, Marine Drive, Mumbai", "89, Connaught Place, Delhi",
    "12, Anna Salai, Chennai", "34, Banjara Hills, Hyderabad"
]

with app.app_context():
    # Get a random project id if available
    project = Project.query.first()
    project_id = project.id if project else None

    for name in names:
        phone = str(random.randint(6000000000, 9999999999))
        daily_wage = random.choice([500.0, 600.0, 700.0, 800.0])
        fixed_salary = random.choice([12000.0, 15000.0, 18000.0, 20000.0])
        address = random.choice(addresses)
        
        new_labour = Labour(
            name=name,
            phone=phone,
            daily_wage=daily_wage,
            fixed_salary=fixed_salary,
            address=address,
            project_id=project_id
        )
        db.session.add(new_labour)
    
    db.session.commit()
    print(f"Added {len(names)} random labourers.")
