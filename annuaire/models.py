from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum

from .views import app
# Create database connection object
db = SQLAlchemy(app)

class Role(enum.Enum):
    guest = 0
    user = 1
    admin = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    picture = db.Column(db.Text(65000), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    role = db.Column(db.Enum(Role), nullable=False, default=Role['user'])

    def __init__(self, firstname, lastname, email, password, role = Role['user']):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role

def init_db():
    db.drop_all()
    db.create_all()

    # Seeding
    db.session.add(User("Admin", "Admin", "admin@admin", "password", Role['admin']))
    db.session.add(User("John", "Doe", "john.doe@example.com", "password"))
    db.session.commit()

    lg.info('Database initialized!')