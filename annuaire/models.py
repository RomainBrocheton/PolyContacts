from flask import Flask
from sqlalchemy import Column, String, Integer
from .base import Session, engine, Base
import logging as lg
import bcrypt

app = Flask(__name__)
app.config.from_object('config')

Base.metadata.create_all(engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(200), nullable=False)
    lastname = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    description = Column(String(200), nullable=True)
    picture = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)

    role = Column(String(4), nullable=False, default=0)

 


def init_db():
    print("init_db")
    seed = True

    # Create table
    Base.metadata.create_all(engine)

    if seed:
        session.execute('TRUNCATE TABLE users')
        session.commit()

        # Seeding
        hashed = bcrypt.hashpw(b"password", bcrypt.gensalt())
        session.add(User(firstname="Admin", lastname="Admin", email="admin@admin", password=hashed, role=2))
        session.add(User(firstname="John", lastname="Doe", email="john@doe", password=hashed))
        session.commit()
        session.close()