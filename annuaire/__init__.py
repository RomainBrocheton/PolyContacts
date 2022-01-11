import os
from flask import Flask

from .views import app
from . import models

models.init_db()