from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import sys

app = Flask(__name__)
app.config.from_object('config')

# Connect sqlalchemy to app
while True:
    try:
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("base.py - Trying again in 5 seconds")
        time.sleep(5)
        continue
    break

Session = sessionmaker(bind=engine)
Base = declarative_base()