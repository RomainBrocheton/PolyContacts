from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object('config')

# Connect sqlalchemy to app
while True:
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    except:
        continue
    break

Session = sessionmaker(bind=engine)
Base = declarative_base()