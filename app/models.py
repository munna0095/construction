from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False) # admin, supervisor, accountant

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_reset_token(self):
        from itsdangerous import URLSafeTimedSerializer
        from flask import current_app
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
        from flask import current_app
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'<User {self.email}>'

class Labour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False) # Exactly 10 digits
    address = db.Column(db.Text) # Full address / Description
    daily_wage = db.Column(db.Float, nullable=False)
    fixed_salary = db.Column(db.Float, default=0.0)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True) # Optional link
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attendances = db.relationship('Attendance', backref='labour', lazy=True)

    def __repr__(self):
        return f'<Labour {self.name}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    labour_id = db.Column(db.Integer, db.ForeignKey('labour.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False)  # 'Present', 'Absent'
    daily_wage = db.Column(db.Float, default=0.0) # Added in Phase 6 for per-day tracking
    advance = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Attendance {self.labour_id} {self.date} {self.status}>'

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False) # e.g., kg, bags, cum
    stock_quantity = db.Column(db.Float, default=0.0)
    unit_price = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True) # Linked to project
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Material {self.name}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Planning') # Planning, In Progress, Completed
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='project', lazy=True)
    labours = db.relationship('Labour', backref='project', lazy=True)
    materials = db.relationship('Material', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=True)
    type = db.Column(db.String(20), nullable=False) # 'IN', 'OUT', 'EXPENSE'
    quantity = db.Column(db.Float, nullable=True) # Now Optional
    total_cost = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending') # 'Paid', 'Pending'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(250))

    # Relationships
    material = db.relationship('Material', backref='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.id}>'

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_email = db.Column(db.String(120), nullable=True)
    reminder_time = db.Column(db.String(5), default='19:00') # "HH:MM" format
    email_sent_date = db.Column(db.Date, nullable=True) # To prevent multiple emails per day

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
